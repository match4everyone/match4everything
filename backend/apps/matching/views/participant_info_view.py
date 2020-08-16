import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from apps.matching.forms import ParticipantInfoViewForm
from apps.matching.models import ParticipantInfo

logger = logging.getLogger(__name__)


@method_decorator([login_required], name="dispatch")
class ParticipantInfoViewView(UpdateView):
    """Updates the information of either participant."""

    template_name = "participant/participant_info_view_form.html"
    slug_url_kwarg = "uuid"
    slug_field = "uuid"

    def dispatch(self, *args, **kwargs):
        url_p_type = self.kwargs["p_type"]
        user_from_url = get_object_or_404(
            ParticipantInfo[url_p_type], uuid=kwargs["uuid"]
        ).participant.user
        user = self.request.user

        # One can view this profile if either:
        # it's yourself
        is_own_profile = user == user_from_url
        # or the configuration in match4everyone/configuration/[A|B] allows it for this type
        # and you are approved (in systems without approval strategies, everyone is approved)
        # or you have the permission to approve or delete users and were given access to also
        # view the details
        has_permission_to_view = (
            user.has_perm("matching.can_view_%s" % url_p_type.lower()) and user.is_approved()
        )

        if is_own_profile or has_permission_to_view:
            return super(ParticipantInfoViewView, self).dispatch(*args, **kwargs)
        else:
            raise PermissionDenied

    def get_form_class(self):
        return ParticipantInfoViewForm[self.kwargs["p_type"]]

    def get_queryset(self):
        return ParticipantInfo[self.kwargs["p_type"]].objects.all()

    def get_success_url(self):
        return reverse("profile")
