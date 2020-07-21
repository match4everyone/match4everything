from datetime import datetime
import uuid

from django.db import models
from django.urls import reverse

from match4everyone.configuration.A import A
from match4everyone.configuration.B import B

from .participant import Participant


class AbstractParticipantInfo(models.Model):
    """
    A participant of the matching process.

    This contains all the configurable properties that can be used for matching participants to one another.
    Defined in the json config.
    """

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    @classmethod
    def excluded_fields(cls):
        return ["uuid", "registration_date", "participant"]

    @classmethod
    def private_fields(cls):
        """Fields that should not be seen by other participants."""
        return cls._private_fields() + cls.excluded_fields()

    @classmethod
    def generate_fake(cls, participant, rs=None):
        """Generate a fake with random data, which is generated according to the p_type of its properties."""
        props = {}
        for field, value in cls._generate_random_values():
            props[field] = value
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
two instances with the same helper - the method that is used for forms etc.
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


ParticipantInfo = {
    "A": ParticipantInfoA,
    "B": ParticipantInfoB,
}


def add_participant_specific_info(name, participant_config):
    """
    Generate Info Table fields from config.

    Programmatically add fields that are defined in the config for the
    respective participant.
    """
    info_cls = ParticipantInfo[name]
    participant_config = participant_config

    properties = participant_config.get_model_fields()

    for field_name, model_field in properties:
        info_cls.add_to_class(field_name, model_field)

    info_cls.add_to_class("_generate_random_values", participant_config.generate_random_assignment)
    info_cls.add_to_class("_private_fields", participant_config.get_private_fields)


add_participant_specific_info("A", A)
add_participant_specific_info("B", B)
