import logging

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.urls import reverse

logger = logging.getLogger(__name__)


@method_decorator([login_required], name="dispatch")
class LoginRedirect(View):
    def get(self, request):
        user = request.user

        if user.is_participant:
            return HttpResponseRedirect(reverse("profile", kwargs={'p_type': user.participant().type()}))

        elif user.is_staff:
            return HttpResponseRedirect("profile_staff")
        else:
            logger.warning(
                "User is unknown type, login redirect not possible", extra={"request": request},
            )
            raise Http404()
