from datetime import datetime
import urllib
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
import django_filters

from apps.matching.data.map_data import zipcodes  # noqa
from apps.matching.utils.map import get_plzs_close_to

from .participant_info import ParticipantInfo
from .participant_info_location import CountryCodeChoices, ParticipantInfoLocation, RadiusChoices
from .user import User


def filter_name():
    """Return a default value for a filter name."""
    return "Old contact request"


class AbstractParticipantInfoFilter(models.Model):
    """A filter that contains information with which the info of a participant can be filtered."""

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    filter_name = models.CharField(max_length=100, default=filter_name)
    subject = models.CharField(max_length=300, blank=True)
    contact_text = models.CharField(max_length=500, blank=True)

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

    def as_get_params(self, seperate_location=False):
        get_request = {}
        location = {}
        for filter_field in self.filter_fields:
            value = getattr(self, filter_field)
            if value is not None:
                if "location_" in filter_field:
                    location[filter_field] = value
                else:
                    split_vers = filter_field.split("-")
                    fieldname = "-".join(split_vers[:-1])
                    lookup_exp = split_vers[-1]
                    if lookup_exp == "exact":
                        get_request[fieldname] = str(value)
                    else:
                        get_request[fieldname + "__" + lookup_exp] = str(value)
        if seperate_location:
            return get_request, location
        return {**get_request, **location}

    @classmethod
    def create_from_filterset(cls, filter_kwargs, created_by):
        filter_kwargs_update = {}
        import django.forms as forms

        class Filter(forms.ModelForm):
            class Meta:
                model = ParticipantInfoFilter[cls.participant_type]
                exclude = ParticipantInfoFilter[cls.participant_type].excluded_fields() + [
                    "subject",
                    "contact_text",
                    "filter_name",
                ]

        for name, value in filter_kwargs.items():
            if "__" not in name and "location_" not in name:
                name = name + "-" + "exact"
            else:
                name = name.replace("__", "-")

            filter_kwargs_update[name] = value

        f = Filter(filter_kwargs_update).save(commit=False)
        f.created_by = created_by
        return f

    def search_url(self):
        url = reverse("participant_list", kwargs={"p_type": self.participant_type})
        params = urllib.parse.urlencode(self.as_get_params())
        return url + "?%s" % params

    @property
    def as_HTML(self):
        general_properties_html = '<ul class="list-group">'
        for filter_field in self.filter_fields:
            if getattr(self, filter_field) is not None:
                try:
                    # there might be an explicit name for the filter_field
                    value = getattr(self, "get_" + filter_field + "_display")()
                except AttributeError:
                    value = getattr(self, filter_field)
                if "location_" in filter_field:
                    pass
                else:
                    general_properties_html += '<li class="list-group-item">'
                    general_properties_html += (
                        self.filter_field_descriptors[filter_field]
                        + " "
                        + str(self.filter_field_labels[filter_field])
                        + ' "'
                        + str(value)
                        + '".'
                    )
                    general_properties_html += "</li>"

        general_properties_html += f'<li class="list-group-item">The location was not further than {self.location_distance}km from {self.location_zipcode} in {self.location_country_code}.</li>'
        general_properties_html += "</ul>"

        return general_properties_html


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


class LocationFilter:
    location_prefix = "location_"

    def is_valid(self, form, p_type):
        prefix = self.location_prefix
        if form.cleaned_data[prefix + "country_code"] not in CountryCodeChoices.values:
            form.add_error(prefix + "country_code", _("You need to provide a valid country code."))
            return False

        if (
            form.cleaned_data[prefix + "zipcode"]
            not in zipcodes[form.cleaned_data[prefix + "country_code"]]
        ):
            form.add_error(
                prefix + "zipcode",
                str(form.cleaned_data[prefix + "zipcode"])
                + str(_(" is not a postcode in "))
                + form.cleaned_data[prefix + "country_code"],
            )
            return False

        if int(form.cleaned_data[prefix + "distance"]) > ParticipantInfoLocation[p_type].MAX_RADIUS:
            distance = form.cleaned_data[prefix + "distance"]
            form.add_error(
                prefix + "distance",
                _(
                    f"You can only search within a radius of {distance} km. Please decrease the radius or change your position."
                ),
            )
            return False
        return True

    def filter_queryset(self, location_query, p_type, qs):
        if qs is None:
            qs = ParticipantInfo[p_type].objects.all()

        return self.__class__.filter_location(location_query, qs=qs)

    @classmethod
    def filter_location(cls, location_query, qs):

        country_code = location_query[cls.location_prefix + "country_code"]
        zipcode = location_query[cls.location_prefix + "zipcode"]
        distance = int(location_query[cls.location_prefix + "distance"])

        if distance == 0:
            close_zipcodes = [zipcode]
        else:
            distance_in_km = distance
            close_zipcodes = get_plzs_close_to(country_code, zipcode, distance_in_km)
        return qs.filter(location__plz__in=close_zipcodes, location__country_code=country_code)


def add_participant_specific_filters(p_type, participant_config):
    """
    Generate filter fields from config.

    Programmatically add fields that are defined in the config for the
    respective participant.
    """
    filter_cls = ParticipantInfoFilter[p_type]

    properties = participant_config.get_filter_fields()

    filter_fields = []
    filter_field_labels = {}
    filter_field_descriptors = {}
    filter_dict = {}

    private_fields = participant_config.get_private_fields()

    for field_name, filters in properties:
        if field_name not in private_fields:
            filter_dict[field_name] = []
            for f in filters:
                filter_field_name = field_name + "-" + f["lookup_exp"]
                filter_field_descriptors[filter_field_name] = f["description"]
                filter_field_labels[filter_field_name] = f["label"]
                filter_cls.add_to_class(filter_field_name, f["model_field"])
                filter_fields.append(filter_field_name)

                filter_dict[field_name].append(f["lookup_exp"])

    filter_fields = filter_fields + [
        "location_country_code",
        "location_zipcode",
        "location_distance",
    ]

    filter_cls.add_to_class("filter_fields", filter_fields)
    filter_cls.add_to_class("filter_field_labels", filter_field_labels)
    filter_cls.add_to_class("filter_field_descriptors", filter_field_descriptors)
    filter_cls.add_to_class(
        "location_country_code", models.CharField(choices=CountryCodeChoices.choices, max_length=2)
    )
    filter_cls.add_to_class("location_zipcode", models.IntegerField())
    filter_cls.add_to_class("location_distance", models.IntegerField(choices=RadiusChoices.choices))

    class ParticipantInfoFilterSetP(django_filters.rest_framework.FilterSet):
        # so far I could not find another method to integrate fields from the filter into the
        # filterset automatically
        location_country_code = django_filters.ChoiceFilter(
            field_name="country_code",
            lookup_expr="exact",
            label=_("Countrycode"),
            choices=CountryCodeChoices.choices,
            initial=CountryCodeChoices.GERMANY,
            required=True,
        )
        location_zipcode = django_filters.CharFilter(
            field_name="plz",
            lookup_expr="exact",
            label=_("Zipcode"),
            initial="14482",
            required=True,
        )
        location_distance = django_filters.ChoiceFilter(
            field_name="distance",
            label=_("Distance"),
            required=True,
            initial=RadiusChoices.LESSTEN,
            choices=RadiusChoices.choices,
        )

        location_filter = LocationFilter()

        class Meta:
            model = ParticipantInfo[p_type]
            fields = filter_dict

        @classmethod
        def filter_spec(cls):
            return filter_dict

        @classmethod
        def add_to_class(cls, value, name):
            return setattr(cls, value, name)

        def is_valid(self):
            valid = super().is_valid()
            if valid:
                return self.location_filter.is_valid(self.form, p_type)
            return valid

        def filter_queryset(self, queryset):
            location_query = {}
            for name, value in self.form.cleaned_data.items():
                # ignore the values that belong to the filter
                if not str.startswith(name, self.location_filter.location_prefix):
                    queryset = self.filters[name].filter(queryset, value)
                    assert isinstance(queryset, models.QuerySet), (
                        "Expected '%s.%s' to return a QuerySet, but got a %s instead."
                        % (type(self).__name__, name, type(queryset).__name__)
                    )
                else:
                    location_query[name] = value
            return self.location_filter.filter_queryset(location_query, p_type=p_type, qs=queryset)

    ParticipantInfoFilterSet[p_type] = ParticipantInfoFilterSetP


add_participant_specific_filters("A", settings.PARTICIPANT_SETTINGS["A"])
add_participant_specific_filters("B", settings.PARTICIPANT_SETTINGS["B"])
