import urllib

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import View

from apps.matching.models import ParticipantInfoFilter


@method_decorator([login_required], name="dispatch")
class ParticipantFilterSearchAgain(View):
    def get(self, request, p_type, uuid):
        filter_ = get_object_or_404(ParticipantInfoFilter[p_type], uuid=uuid)
        url = reverse("participant_list", kwargs={"p_type": self.kwargs["p_type"]})
        params = urllib.parse.urlencode(filter_.as_get_params())
        return HttpResponseRedirect(url + "?%s" % params)
