from datetime import datetime
import json
import uuid

from django.db import models
from django.urls import reverse

from .participant import Participant
from .participant_info_properties import create_property


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


def add_participant_specific_info(name, config):
    """
    Generate Info Table fields from config.

    Programmatically add fields that are defined in the config for the
    respective participant.
    """
    info_cls = ParticipantInfo[name]

    labels = {c["field_name"]: c["label"] for c in config["info"]}
    properties = [create_property(c) for c in config["info"]]

    for p in properties:
        info_cls.add_to_class(p.field_name, p.get_field())

    info_cls.add_to_class("column_labels", labels)
    info_cls.add_to_class(
        "random_generators", {p.field_name: p.get_random_value for p in properties}
    )


with open("match4everyone/config/participant_info.json") as json_file:
    info_config = json.load(json_file)

add_participant_specific_info("A", info_config["A"])
add_participant_specific_info("B", info_config["B"])
