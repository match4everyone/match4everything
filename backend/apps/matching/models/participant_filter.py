from datetime import datetime
import uuid

from django.db import models
from django.urls import reverse
import django_filters

from match4everyone.config.A import A

from .participant_info import ParticipantInfo


class AbstractParticipantInfoFilter(models.Model):
    """A filter that contains information with which the info of a participant can be filtered."""

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    @staticmethod
    def excluded_fields():
        return ["uuid", "registration_date", "participant"]

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse("info-filter", kwargs={"uuid": self.uuid, "p_type": self.participant_type})

    def as_get_params(self):
        get_request = {}
        for filter_field in self.filter_fields:
            value = getattr(self, filter_field)
            if value is not None:
                split_vers = filter_field.split("-")
                fieldname = "-".join(split_vers[:-1])
                lookup_exp = split_vers[-1]
                if lookup_exp == "exact":
                    get_request[fieldname] = str(value)
                else:
                    get_request[fieldname + "__" + lookup_exp] = str(value)
        return get_request


"""
Unfortunately, primary keys cannot be added programatically,
which is why we need to explicitly define the classes instead of generating
two instances with the same helper - tha method that is used for forms etc.
"""


class ParticipantInfoFilterA(AbstractParticipantInfoFilter):
    participant_type = "A"


class ParticipantInfoFilterB(AbstractParticipantInfoFilter):
    participant_type = "B"


ParticipantInfoFilter = {"A": ParticipantInfoFilterA, "B": ParticipantInfoFilterB}

ParticipantInfoFilterSet = {}


def add_participant_specific_filters(name, participant_config):
    """
    Generate filter fields from config.

    Programmatically add fields that are defined in the config for the
    respective participant.
    """
    filter_cls = ParticipantInfoFilter[name]
    participant_config = participant_config()

    properties = participant_config.get_filter_fields()
    filter_fields = []
    filter_dict = {}

    for field_name, filters in properties:
        filter_dict[field_name] = []
        for f in filters:
            filter_field_name = field_name + "-" + f["lookup_exp"]
            filter_cls.add_to_class(filter_field_name, f["model_field"])
            filter_fields.append(filter_field_name)

            filter_dict[field_name].append(f["lookup_exp"])

    filter_cls.add_to_class("filter_fields", filter_fields)

    class ParticipantInfoFilterSetP(django_filters.FilterSet):
        class Meta:
            model = ParticipantInfo[name]
            fields = filter_dict

        @classmethod
        def filter_spec(cls):
            return filter_dict

    ParticipantInfoFilterSet[name] = ParticipantInfoFilterSetP


add_participant_specific_filters("A", A)
add_participant_specific_filters("B", A)  # add an own file for B as soon as someone writes it
