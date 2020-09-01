from datetime import datetime
import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.matching.dummy_mail.mail import send_email

from .participant import ParticipantA, ParticipantB
from .participant_filter import (
    LocationFilter,
    ParticipantInfo,
    ParticipantInfoFilterA,
    ParticipantInfoFilterB,
)


class MATCH_STATE_OPTIONS:
    CONTACTED = 1
    SUCCESSFUL = 2
    NOT_SUCCESSFUL = 3
    DECLINE = 4


MATCH_STATE = [
    (MATCH_STATE_OPTIONS.CONTACTED, _("contacted")),
    (MATCH_STATE_OPTIONS.SUCCESSFUL, _("successful")),
    (MATCH_STATE_OPTIONS.NOT_SUCCESSFUL, _("not successful")),
    (MATCH_STATE_OPTIONS.DECLINE, _("declined")),
]


class Match(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    participantA = models.ForeignKey(ParticipantA, on_delete=models.CASCADE, related_name="match")
    participantB = models.ForeignKey(ParticipantB, on_delete=models.CASCADE, related_name="match")

    initiator = models.CharField(choices=[("A", "A"), ("B", "B")], max_length=1)
    match_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    state = models.IntegerField(choices=MATCH_STATE, default=MATCH_STATE_OPTIONS.CONTACTED)

    filterA = models.ForeignKey(
        ParticipantInfoFilterA, on_delete=models.SET(None), null=True, blank=True
    )
    filterB = models.ForeignKey(
        ParticipantInfoFilterB, on_delete=models.SET(None), null=True, blank=True
    )

    response_subject = models.CharField(max_length=300, blank=True, null=True)
    response_message = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["state", "match_date"]

    @property
    def contacted_via_filter(self):
        if self.filterA is not None:
            return self.filterA, "A"
        if self.filterB is not None:
            return self.filterB, "B"
        # filter was deleted after the match
        # or not used for finding the match
        return None, None

    @property
    def filter_url(self):
        filter_, p_type = self.contacted_via_filter
        if filter_ is not None:
            return filter_.search_url()
        return ""

    @property
    def filter_uuid(self):
        return self.contacted_via_filter[0].uuid

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
    def contact_all_not_matched_to(cls, this_filter):
        normal_filter, location_filter = this_filter.as_get_params(seperate_location=True)

        qs = ParticipantInfo[this_filter.participant_type].objects.filter(**normal_filter)
        matches = LocationFilter.filter_location(location_filter, qs)

        if this_filter.participant_type == "A":
            not_yet_contacted = matches.filter(
                ~models.Q(participant__match__participantB=this_filter.created_by.participant())
            )

            for participant_info in not_yet_contacted:
                m = Match.objects.create(
                    participantA=participant_info.participant,
                    participantB=this_filter.created_by.participant(),
                    filterA=this_filter,
                    initiator="B",
                )
                m.send_contact_request()
                m.save()

        else:
            not_yet_contacted = matches.filter(
                ~models.Q(participant__match__participantA=this_filter.created_by.participant())
            )

            for participant_info in not_yet_contacted:
                m = Match.objects.create(
                    participantB=participant_info.participant,
                    participantA=this_filter.created_by.participant(),
                    filterB=this_filter,
                    initiator="A",
                )
                m.send_contact_request()
                m.save()

    def send_response(self, subject, message):
        self.state = MATCH_STATE_OPTIONS.SUCCESSFUL
        self.response_subject = subject
        self.response_message = message
        send_email(
            to_participant=self.initiator_participant(),
            from_participant=self.requested_participant(),
            subject=subject,
            message=message,
            email_type="response",
        )
        self.save()

    def send_contact_request(self):
        subject, message = self.inital_message
        send_email(
            to_participant=self.requested_participant(),
            from_participant=self.initiator_participant(),
            subject=subject,
            message=message,
            email_type="contact_request",
        )

    @classmethod
    def matches_to(cls, this_filter):

        normal_filter, location_filter = this_filter.as_get_params(seperate_location=True)
        qs = ParticipantInfo[this_filter.participant_type].objects.filter(**normal_filter)
        matches = LocationFilter.filter_location(location_filter, qs)

        available_matches = matches.count()
        if this_filter.participant_type == "A":
            already_contacted_with_via_filter = matches.filter(
                participant__match__filterA=this_filter
            ).count()
            already_in_contact_with = matches.filter(
                participant__match__participantB=this_filter.created_by.participant()
            ).count()

        else:
            already_contacted_with_via_filter = matches.filter(
                participant__match__filterB=this_filter
            ).count()
            already_in_contact_with = (
                matches.filter(
                    participant__match__participantA=this_filter.created_by.participant()
                )
                .distinct()
                .count()
            )

        return (already_in_contact_with, already_contacted_with_via_filter, available_matches)

    @property
    def email_initiator(self):
        return self.initiator_participant().user.email

    @property
    def email_initiator_url(self):
        p = self.initiator_participant().user.participant()
        return reverse("info-view", kwargs={"uuid": p.info.uuid, "p_type": p.participant_type})

    @property
    def email_receiver(self):
        if self.state in [MATCH_STATE_OPTIONS.SUCCESSFUL, MATCH_STATE_OPTIONS.NOT_SUCCESSFUL]:
            return self.requested_participant().user.email
        elif self.state == MATCH_STATE_OPTIONS.DECLINE:
            return _("the other participant declined your offer")
        return _("waiting for response")

    @property
    def email_receiver_url(self):
        p = self.requested_participant().user.participant()
        return (
            True,
            reverse("info-view", kwargs={"uuid": p.info.uuid, "p_type": p.participant_type}),
        )

    @property
    def inital_message(self):
        filter_, participant = self.contacted_via_filter
        if filter_ is None:
            return "", ""
        return filter_.subject, filter_.contact_text
