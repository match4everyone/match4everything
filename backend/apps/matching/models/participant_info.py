from datetime import datetime
import json
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
import django_filters

from .participant import Participant
from .participant_info_properties import create_property
from .user import User


class AbstractParticipantInfo(models.Model):
    """
    A participant of the matching process.

    This contains all the configurable properties that can be used for matching participants to one another.
    Defined in the json config.
    """

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    @staticmethod
    def private_fields():
        return ["uuid", "registration_date", "participant"]

    @classmethod
    def generate_fake(cls, participant, rs=None):
        """Generate a fake with random data, which is generated according to the p_type of its properties."""
        props = {}
        for field, generator in cls.random_generators.items():
            props[field] = generator(rs)
        p = cls.objects.create(participant=participant, **props)
        p.save()
        return p

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse("info-edit", kwargs={"uuid": self.uuid, "p_type": self.participant_type})


"""
Unfortunately, primary keys cannot be added programatically,
which is why we need to explicitly define the classes instead of generating
two instances with the same helper the is used for forms etc.
"""


class ParticipantInfoA(AbstractParticipantInfo):
    participant_type = "A"
    participant = models.OneToOneField(
        Participant["A"], on_delete=models.CASCADE, primary_key=True, related_name="info"
    )


class ParticipantInfoB(AbstractParticipantInfo):
    participant_type = "B"
    participant = models.OneToOneField(
        Participant["B"], on_delete=models.CASCADE, primary_key=True, related_name="info"
    )


ParticipantInfo = {"A": ParticipantInfoA, "B": ParticipantInfoB}


class ParticipantInfoFilterA(models.Model):
    participant_type = "A"
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def as_get_params(self):
        get_request = {}
        for filter_field in self.filter_fields:
            value = getattr(self, filter_field)
            if value is not None:
                lookup_name = filter_field.replace("-", "__")
                if lookup_name.split("__")[1] == "exact":
                    get_request[lookup_name.split("__")[0]] = str(value)
                else:
                    get_request[filter_field.replace("-", "__")] = str(value)
        return get_request


class ParticipantInfoFilterB(models.Model):
    participant_type = "B"
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def as_get_params(self):
        get_request = {}
        for filter_field in self.filter_fields:
            value = getattr(self, filter_field)
            if value is not None:
                lookup_name = filter_field.replace("-", "__")
                if lookup_name.split("__")[1] == "exact":
                    get_request[lookup_name.split("__")[0]] = str(value)
                else:
                    get_request[filter_field.replace("-", "__")] = str(value)
        return get_request


ParticipantInfoFilter = {"A": ParticipantInfoFilterA, "B": ParticipantInfoFilterB}
ParticipantInfoFilterSet = {}


def add_participant_specific_info(name, config):
    """
    Generate Info Table fields from config.

    Programmatically add fields that are defined in the config for the
    respective participant.
    """
    # Create the participant info
    info_cls = ParticipantInfo[name]

    labels = {c["field_name"]: c["label"] for c in config["info"]}
    properties = [create_property(c) for c in config["info"]]

    for p in properties:
        info_cls.add_to_class(p.field_name, p.get_field())

    info_cls.add_to_class("column_labels", labels)
    info_cls.add_to_class(
        "random_generators", {p.field_name: p.get_random_value for p in properties}
    )

    # Create the persistent filter and filter set for the participant info
    filter_cls = ParticipantInfoFilter[name]
    filter_fields = []
    for p in properties:
        filters = p.get_filters()
        for filter_props in filters:
            filter_field_name = p.field_name + "-" + filter_props["lookup_exp"]
            filter_cls.add_to_class(filter_field_name, filter_props["model_field"])
            filter_fields.append(filter_field_name)

    filter_cls.add_to_class("filter_fields", filter_fields)

    # refer to https://django-filter.readthedocs.io/en/latest/ref/filterset.html for deeper insight
    filter_set_fields = {}
    for p in properties:
        filter_set_fields[p.field_name] = [props["lookup_exp"] for props in p.get_filters()]

    class ParticipantInfoFilterSetP(django_filters.FilterSet):
        class Meta:
            model = ParticipantInfo[name]
            fields = filter_set_fields

        @classmethod
        def filter_spec(cls):
            return filter_set_fields

    ParticipantInfoFilterSet[name] = ParticipantInfoFilterSetP


with open(f"{settings.BASE_DIR}/match4everyone/config/participant_info.json") as json_file:
    info_config = json.load(json_file)

add_participant_specific_info("A", info_config["A"])
add_participant_specific_info("B", info_config["B"])
