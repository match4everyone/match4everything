import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from apps.matching.admin import m4e_staff_member_required

logger = logging.getLogger(__name__)


@method_decorator([login_required, m4e_staff_member_required], name="dispatch")
class StaffProfileView(TemplateView):
    template_name = "staff/staff_profile.html"

    def get_context_data(self, **kwargs):
        return {
            "A_requires_approval": settings.PARTICIPANT_SETTINGS[
                "A"
            ].needs_manual_approval_from_staff,
            "B_requires_approval": settings.PARTICIPANT_SETTINGS[
                "B"
            ].needs_manual_approval_from_staff,
        }
