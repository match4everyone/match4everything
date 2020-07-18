import logging

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from apps.matching.admin import (
    profile_visible_for_A,
    profile_visible_for_B,
    profile_visible_for_other_A,
    profile_visible_for_other_B,
    required_at_least_one,
)
from apps.matching.forms import ParticipantViewInfoForm
from apps.matching.models import ParticipantInfo
from match4everyone.configuration.A import A
from match4everyone.configuration.B import B

logger = logging.getLogger(__name__)

restrictions_A = []
restrictions_B = []
if A.profile_visible_for_B:
    restrictions_A.append(profile_visible_for_B)
if A.profile_visible_for_other_A:
    restrictions_A.append(profile_visible_for_other_A)

if B.profile_visible_for_A:
    restrictions_B.append(profile_visible_for_A)
if B.profile_visible_for_other_B:
    restrictions_B.append(profile_visible_for_other_B)

decorators = [login_required, required_at_least_one(restrictions_A, restrictions_B)]


@method_decorator(decorators, name="dispatch")
class ParticipantInfoViewView(UpdateView):
    """Updates the information of either participant."""

    template_name = "participant/participant_info_view_form.html"
    slug_url_kwarg = "uuid"
    slug_field = "uuid"

    def get_form_class(self):
        return ParticipantViewInfoForm[self.kwargs["p_type"]]

    def get_queryset(self):
        return ParticipantInfo[self.kwargs["p_type"]].objects.all()

    def get_success_url(self):
        return reverse("profile")
