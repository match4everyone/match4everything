import logging

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from apps.matching.forms import ParticipantViewInfoForm
from apps.matching.models import ParticipantInfo
from match4everyone.configuration.A import A
from match4everyone.configuration.B import B

logger = logging.getLogger(__name__)

decorators = [login_required]
if A.profile_visible_for_B:
    decorators.append(None)
if A.profile_visible_for_other_A:
    decorators.append(None)
if B.profile_visible_for_A:
    decorators.append(None)
if B.profile_visible_for_other_B:
    decorators.append(None)


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
