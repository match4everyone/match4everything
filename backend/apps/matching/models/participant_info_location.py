from django.db import models
from .participant_info import ParticipantInfo
from django.utils.translation import gettext_lazy as _
from apps.matching.files.map_data import plzs
from django.core.exceptions import ValidationError
import numpy as np
from apps.matching.src.plzs import BIG_CITY_PLZS
from datetime import datetime
import uuid


class RadiusChoices(models.IntegerChoices):
    LESSTEN = 10, _("<10 km")
    LESSTWENTY = 20, _("<20 km")
    LESSFOURTY = 30, _("<40 km")
    MOREFOURTY = 40, _(">40 km")


class CountryCode(models.TextChoices):
    GERMANY = "DE", _("Germany")
    AUSTRIA = "AT", _("Austria")


class AbstractParticipantInfoLocation(models.Model):
    """
    Gives information about the location availability of a participant.

    Only for Germany and Austria.
    """

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    country_code = models.CharField(max_length=2, choices=CountryCode.choices, default=CountryCode.GERMANY)
    plz = models.CharField(max_length=5, null=True)
    radius = models.IntegerField(choices=RadiusChoices.choices, default=RadiusChoices.LESSFOURTY, blank=False)

    def clean(self):
        if self.plz not in plzs[self.country_code]:
            raise ValidationError(
                str(self.plz) + str(_(" is not a postcode in ")) + self.country_code
            )

    class Meta:
        abstract = True

    @classmethod
    def generate_fake(cls, participant_info, rs=np.random):
        pil = cls.objects.create(participant_info=participant_info,
                                 country_code='DE',
                                 plz=rs.choice(BIG_CITY_PLZS))
        pil.save()
        return pil


class ParticipantInfoLocationA(AbstractParticipantInfoLocation):
    participant_type = "A"
    participant_info = models.OneToOneField(ParticipantInfo["A"], on_delete=models.CASCADE, primary_key=True,
                                            related_name='location')


class ParticipantInfoLocationB(AbstractParticipantInfoLocation):
    participant_type = "B"
    participant_info = models.OneToOneField(ParticipantInfo["B"], on_delete=models.CASCADE, primary_key=True,
                                            related_name='location')


ParticipantInfoLocation = {
    "A": ParticipantInfoLocationA,
    "B": ParticipantInfoLocationB
}
