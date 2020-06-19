import logging

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import TemplateView

from apps.matching.admin import participant_check

logger = logging.getLogger(__name__)

"""
View the dashboard of a participant
"""


class ParticipantDashboard(TemplateView, UserPassesTestMixin):
    def test_func(self):
        return participant_check(self.request.user)

    template_name = "participant/participant_dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ParticipantDashboard, self).get_context_data(*args, **kwargs)
        context["participant"] = self.request.user.participant()
        context["uuid"] = self.request.user.participant().info.uuid
        context["p_type"] = self.request.user.participant().participant_type
        return context
