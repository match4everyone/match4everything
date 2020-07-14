import logging

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

logger = logging.getLogger(__name__)


@method_decorator([login_required], name="dispatch")
class ProfileDashboardRedirect(View):
    """Redirect to the correct place on clicking profile."""

    def get(self, request):
        user = request.user

        if user.is_participant:
            return HttpResponseRedirect(reverse("profile"))
        elif user.is_staff:
            return HttpResponseRedirect(reverse("profile_staff"))

        else:
            logger.warning(
                "User is unknown type, profile redirect not possible", extra={"request": request},
            )
            return Http404
