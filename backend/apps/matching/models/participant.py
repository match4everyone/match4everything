from datetime import datetime
import uuid

from django.db import models

from .staff import Staff
from .user import User


class AbstractParticipant(models.Model):
    """
    A participant takes part in the matching process.

    In this class everything goes that belongs to maintaining such an account.
    - activation
    - validation
    - stats about the user that are note relevant for matching exactly
    ...

    """

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    # wants to take part in the matching process
    is_activated = models.BooleanField(default=True)

    # valiFdation of account by staff
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    @classmethod
    def _consistent_user(self, email, is_A, is_B):
        return User.new(email, is_participant=True, is_A=is_A, is_B=is_B)

    @classmethod
    def new(cls, participant_type, email, **kwargs):
        is_A = participant_type == "A"
        is_B = participant_type == "B"
        user = cls._consistent_user(email, is_A, is_B)
        participant = cls.objects.create(user=user, **kwargs)
        participant.save()
        return participant

    def p_type(self):
        return self.participant_type

    @staticmethod
    def excluded_fields():
        return ["uuid", "is_approved", "approved_by", "is_activated", "registration_date", "user"]


class ParticipantA(AbstractParticipant):
    participant_type = "A"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="a")


class ParticipantB(AbstractParticipant):
    participant_type = "B"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="b")


Participant = {"A": ParticipantA, "B": ParticipantB}
