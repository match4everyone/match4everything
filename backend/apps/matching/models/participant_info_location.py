from datetime import datetime
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import numpy as np

from apps.matching.data.map_data import zipcodes  # noqa
from apps.matching.utils.zipcodes import GERMAN_BIG_CITY_ZIPCODES  # noqa

from .participant_info import ParticipantInfo


class RadiusChoices(models.IntegerChoices):
    ONLY_HERE = 0, _("0 km")
    LESSTEN = 10, _("<10 km")
    LESSTWENTY = 20, _("<20 km")
    LESSFOURTY = 40, _("<40 km")
    LESSFIFTY = 50, _("<50 km")


class CountryCodeChoices(models.TextChoices):
    GERMANY = "DE", _("Germany")
    AUSTRIA = "AT", _("Austria")


class AbstractParticipantInfoLocation(models.Model):
    """
    Gives information about the location availability of a participant.

    Only for Germany and Austria.
    """

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    country_code = models.CharField(
        max_length=2, choices=CountryCodeChoices.choices, default=CountryCodeChoices.GERMANY
    )
    plz = models.CharField(max_length=5, null=True)
    radius = models.IntegerField(
        choices=RadiusChoices.choices, default=RadiusChoices.LESSFOURTY, blank=False
    )

    def clean(self):
        if self.plz not in zipcodes[self.country_code]:
            raise ValidationError(
                str(self.plz) + str(_(" is not a postcode in ")) + self.country_code
            )

    class Meta:
        abstract = True

    @classmethod
    def generate_fake(cls, participant_info, rs=np.random):
        pil = cls.objects.create(
            participant_info=participant_info,
            country_code="DE",
            plz=rs.choice(GERMAN_BIG_CITY_ZIPCODES),
        )
        pil.save()
        return pil

    @classmethod
    def excluded_fields(cls):
        return ["participant_info", "registration_date", "uuid"]


class ParticipantInfoLocationA(AbstractParticipantInfoLocation):
    participant_type = "A"
    participant_info = models.ForeignKey(
        ParticipantInfo["A"], on_delete=models.CASCADE, related_name="location"
    )
    MAX_RADIUS = settings.PARTICIPANT_SETTINGS["A"].LOCATION_SEARCH_MAX_RADIUS


class ParticipantInfoLocationB(AbstractParticipantInfoLocation):
    participant_type = "B"
    participant_info = models.ForeignKey(
        ParticipantInfo["B"], on_delete=models.CASCADE, related_name="location"
    )
    MAX_RADIUS = settings.PARTICIPANT_SETTINGS["B"].LOCATION_SEARCH_MAX_RADIUS


ParticipantInfoLocation = {
    "A": ParticipantInfoLocationA,
    "B": ParticipantInfoLocationB,
}
