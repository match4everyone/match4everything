import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from apps.matching.models import Match, MATCH_STATE_OPTIONS

logger = logging.getLogger(__name__)

"""
View the dashboard of a participant
"""


@method_decorator([login_required], name="dispatch")
class ParticipantDashboard(TemplateView):
    template_name = "participant/participant_dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ParticipantDashboard, self).get_context_data(*args, **kwargs)
        context["participant"] = self.request.user.participant()
        context["uuid"] = self.request.user.participant().info.uuid
        context["p_type"] = self.request.user.participant().participant_type
        if context["p_type"] == "B":
            context["p_type_opposite"] = "A"
            context["not_responded_to_n_requests"] = Match.objects.filter(
                initiator=context["p_type_opposite"],
                participantB=self.request.user.participant(),
                state=MATCH_STATE_OPTIONS.CONTACTED,
            ).count()
        else:
            context["p_type_opposite"] = "B"
            context["not_responded_to_n_requests"] = Match.objects.filter(
                initiator=context["p_type_opposite"],
                participantA=self.request.user.participant(),
                state=MATCH_STATE_OPTIONS.CONTACTED,
            ).count()

        if not self.request.user.participant().is_activated:
            text = _("Your account is currently deactivated.")
            messages.add_message(self.request, messages.WARNING, text)

        return context
