import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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

    def dispatch(self, *args, **kwargs):
        user_from_url = (
            ParticipantInfo[kwargs["p_type"]]
            .objects.get_or_404(uuid=kwargs["uuid"])
            .participant.user
        )
        user_from_request = self.request.user
        if user_from_request != user_from_url:
            # if (user_from_request == user_from_url):
            # or user has_perm (matching.participant X . can view)
            # or user is of other type and is_approved:
            # return super, else HTTPForbidden
            return HttpResponseForbidden()

        return super(ParticipantInfoViewView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        return ParticipantViewInfoForm[self.kwargs["p_type"]]

    def get_queryset(self):
        return ParticipantInfo[self.kwargs["p_type"]].objects.all()

    def get_success_url(self):
        return reverse("profile")
