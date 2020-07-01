from datetime import datetime
import uuid

from django.db import models
from django.urls import reverse
import django_filters

from match4everyone.config.A import A

from .participant_info import ParticipantInfo
from .user import User


class AbstractParticipantInfoFilter(models.Model):
    """A filter that contains information with which the info of a participant can be filtered."""

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    name = models.CharField(max_length=100)

    @staticmethod
    def excluded_fields():
        return ["uuid", "registration_date", "created_by"]

    class Meta:
        abstract = True
        ordering = ["-registration_date"]

    def get_absolute_url(self):
        return reverse(
            "info-filter-edit", kwargs={"uuid": self.uuid, "p_type": self.participant_type}
        )

    def get_copy(self):
        """In case a user wants to copy an instance they already created."""
        copy = self.__class__.objects.get(id=self.id)
        copy.id = None
        copy.uuid = None
        copy.registration_date = None
        return copy

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

    def matching_infos(self):
        return ParticipantInfo[self.participant_type].objects.filter(**self.as_get_params()).count()

    @classmethod
    def create_from_filterset(cls, filter_kwargs, created_by):
        filter_kwargs_update = {}
        import django.forms as forms

        class Filter(forms.ModelForm):
            class Meta:
                model = ParticipantInfoFilter[cls.participant_type]
                exclude = ParticipantInfoFilter[cls.participant_type].excluded_fields() + ["name"]

        for name, value in filter_kwargs["data"].items():
            if "__" not in name:
                name = name + "-" + "exact"
            else:
                name = name.replace("__", "-")

            filter_kwargs_update[name] = value

        f = Filter(filter_kwargs_update).save(commit=False)
        f.created_by = created_by
        return f
        # return ParticipantInfo[cls.participant_type].objects.create(**filter_kwargs_update)


"""
Unfortunately, primary keys cannot be added programatically,
which is why we need to explicitly define the classes instead of generating
two instances with the same helper - tha method that is used for forms etc.
"""


class ParticipantInfoFilterA(AbstractParticipantInfoFilter):
    participant_type = "A"
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ParticipantInfoFilterB(AbstractParticipantInfoFilter):
    participant_type = "B"
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


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

    private_fields = participant_config.get_private_fields()

    for field_name, filters in properties:
        if field_name not in private_fields:
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
