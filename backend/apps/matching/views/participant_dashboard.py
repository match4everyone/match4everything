from django.views.generic.base import TemplateView
import logging

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.matching.admin import participant_required, matching_participant_required

logger = logging.getLogger(__name__)

"""
View the dashboard of a participant
"""


@method_decorator([login_required, matching_participant_required], name="dispatch")
class ParticipantDashboard(TemplateView):
    template_name = 'participant/participant_dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ParticipantDashboard, self).get_context_data(*args, **kwargs)
        context['participant'] = self.request.user.participant()
        context['uuid'] = self.request.user.participant().info.uuid
        context['p_type'] = self.request.user.participant().participant_type
        return context
