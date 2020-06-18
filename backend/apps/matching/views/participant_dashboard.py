import logging

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from apps.matching.admin import participant_check

logger = logging.getLogger(__name__)

"""
View the dashboard of a participant
"""


@method_decorator([login_required], name="dispatch")
@user_passes_test(participant_check)
class ParticipantDashboard(TemplateView):
    template_name = "participant/participant_dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ParticipantDashboard, self).get_context_data(*args, **kwargs)
        context["participant"] = self.request.user.participant()
        context["uuid"] = self.request.user.participant().info.uuid
        context["p_type"] = self.request.user.participant().participant_type
        return context
