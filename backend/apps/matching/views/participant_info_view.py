import logging

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from apps.matching.admin import matching_participant_required
from apps.matching.forms import ParticipantViewInfoForm
from apps.matching.models import ParticipantInfo

logger = logging.getLogger(__name__)


@method_decorator([login_required, matching_participant_required], name="dispatch")
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
        return reverse("profile", kwargs={"p_type": self.kwargs["p_type"]})
