from datetime import datetime
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .participant import ParticipantA, ParticipantB
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

    participantA = models.ForeignKey(ParticipantA, on_delete=models.CASCADE)
    participantB = models.ForeignKey(ParticipantB, on_delete=models.CASCADE)

    initiator = models.CharField(choices=["A", "B"], max_length=1)
    match_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    state = models.IntegerField(choices=MATCH_STATE, default=CONTACTED)

    filterA = models.ForeignKey(
        ParticipantInfoFilterA, on_delete=models.SET(None), null=True, blank=True
    )
    filterB = models.ForeignKey(
        ParticipantInfoFilterB, on_delete=models.SET(None), null=True, blank=True
    )

    class Meta:
        unique_together = [("participantA", "participantB")]

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
