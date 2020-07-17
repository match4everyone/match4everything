from datetime import datetime
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .participant import Participant, ParticipantA, ParticipantB
from .participant_filter import ParticipantInfoFilterA, ParticipantInfoFilterB

CONTACTED = 1
SUCCESSFUL = 2
NOT_SUCCESSFUL = 3
BLOCKED = 4
MATCH_STATE = [
    (CONTACTED, _("contacted")),
    (SUCCESSFUL, _("successful")),
    (NOT_SUCCESSFUL, _("not successful")),
    (BLOCKED, _("blocked")),
]


class Match(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    participantA = models.ForeignKey(ParticipantA, on_delete=models.CASCADE, related_name="match")
    participantB = models.ForeignKey(ParticipantB, on_delete=models.CASCADE, related_name="match")

    initiator = models.CharField(choices=[("A", "A"), ("B", "B")], max_length=1)
    match_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    state = models.IntegerField(choices=MATCH_STATE, default=CONTACTED)

    filterA = models.ForeignKey(
        ParticipantInfoFilterA, on_delete=models.SET(None), null=True, blank=True
    )
    filterB = models.ForeignKey(
        ParticipantInfoFilterB, on_delete=models.SET(None), null=True, blank=True
    )

    def contacted_via_filter(self):
        if self.filterA is None:
            return self.filterA, "A"
        if self.filterB is None:
            return self.filterB, "B"
        # filter was deleted after the match
        # or not used for finding the match
        return None, None

    def initiator_participant(self):
        if self.initiator == "A":
            return self.participantA
        else:
            return self.participantB

    def requested_participant(self):
        if self.initiator != "A":
            return self.participantA
        else:
            return self.participantB

    @classmethod
    def matches_to(cls, this_filter):

        filter_params = {"info__" + k: v for k, v in this_filter.as_get_params().items()}

        matches = Participant[this_filter.participant_type].objects.filter(**filter_params)
        available_matches = matches.count()
        if this_filter.participant_type == "A":
            already_contacted_with_via_filter = matches.filter(match__filterA=this_filter).count()
            already_in_contact_with = matches.filter(
                match__participantB=this_filter.created_by.participant()
            ).count()

        else:
            already_contacted_with_via_filter = matches.filter(match__filterB=this_filter).count()
            already_in_contact_with = matches.filter(
                match__participantA=this_filter.created_by.participant()
            ).count()

        return (already_in_contact_with, already_contacted_with_via_filter, available_matches)
