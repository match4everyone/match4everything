from datetime import datetime
import uuid

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.utils.translation import gettext as _

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

    # validation of account by staff
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)

    # number of mails a user can send per day
    max_mails_per_day = models.IntegerField(default=settings.MAX_EMAILS_PER_DAY)

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

        # if we do not require approvals, add everyone to the approved group on creation
        if is_A and not settings.PARTICIPANT_SETTINGS["A"].needs_manual_approval_from_staff:
            approved_participants = Group.objects.get(name="approved_a")
            participant.is_approved = True
            participant.approval_date = datetime.now()
            approved_participants.user_set.add(user)
        if is_B and not settings.PARTICIPANT_SETTINGS["B"].needs_manual_approval_from_staff:
            approved_participants = Group.objects.get(name="approved_b")
            participant.is_approved = True
            participant.approval_date = datetime.now()
            approved_participants.user_set.add(user)

        user.save()
        participant.save()

        return participant

    def p_type(self):
        return self.participant_type

    @transaction.atomic
    def change_approval(self, approver):
        p_type = self.p_type().lower()

        # check permission only here in case it was forgotten in the view
        # maybe we can give a nicer message here?
        if not approver.has_perm("matching.can_approve_type_%s" % p_type):
            raise PermissionDenied(_("You currently don't have the permission to approve users."))

        approved_participants = Group.objects.get(name="approved_%s" % p_type)

        if not self.is_approved:
            self.is_approved = True
            self.approval_date = datetime.now()
            self.approved_by = approver
            approved_participants.user_set.add(self.user)
        else:
            self.is_approved = False
            self.approval_date = None
            self.approved_by = None
            approved_participants.user_set.remove(self.user)
        self.save()

    @transaction.atomic
    def increase_mail_limit(self, mail_limit):
        self.max_mails_per_day = mail_limit
        self.save()

    @staticmethod
    def excluded_fields():
        return ["uuid", "is_approved", "approved_by", "is_activated", "registration_date", "user"]

    @property
    def info_uuid(self):
        return self.info.uuid


class ParticipantA(AbstractParticipant):
    participant_type = "A"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="a")


class ParticipantB(AbstractParticipant):
    participant_type = "B"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="b")


Participant = {
    "A": ParticipantA,
    "B": ParticipantB,
}
