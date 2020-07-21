import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from apps.matching.admin import matching_participant_required
from apps.matching.forms import ParticipantInfoViewForm
from apps.matching.models import ParticipantInfo

logger = logging.getLogger(__name__)


@method_decorator([login_required, matching_participant_required], name="dispatch")
class ParticipantInfoViewView(UpdateView):
    """Updates the information of either participant."""

    template_name = "participant/participant_info_view_form.html"
    slug_url_kwarg = "uuid"
    slug_field = "uuid"

    def dispatch(self, *args, **kwargs):
        user_from_url = get_object_or_404(
            ParticipantInfo[self.kwargs["p_type"]], uuid=kwargs["uuid"]
        ).participant.user
        user = self.request.user
        # if user_from_request != user_from_url:
        is_own_profile = user == user_from_url
        has_explicit_permission = user.has_perm("matching.participant.can_view")
        is_other_type_and_approved = False  # TODO
        is_same_type_and_setting_says_so = False  # TODO

        if (
            is_own_profile
            or has_explicit_permission
            or is_other_type_and_approved
            or is_same_type_and_setting_says_so
        ):
            return super(ParticipantInfoViewView, self).dispatch(*args, **kwargs)
        else:
            raise PermissionDenied

    def get_form_class(self):
        return ParticipantInfoViewForm[self.kwargs["p_type"]]

    def get_queryset(self):
        return ParticipantInfo[self.kwargs["p_type"]].objects.all()

    def get_success_url(self):
        return reverse("profile")
