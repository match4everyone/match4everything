import logging
import urllib

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from apps.matching.forms import ParticipantFilterForm

logger = logging.getLogger(__name__)


@method_decorator([login_required], name="dispatch")
class ParticipantFilterCreateView(CreateView):
    """Create a persistent Filter."""

    template_name = "participant/participant_filter_create.html"

    def get_form_class(self):
        return ParticipantFilterForm[self.kwargs["p_type"]]

    def form_valid(self, form):
        info_filter = form.save(commit=False)
        info_filter.created_by = self.request.user
        info_filter.save()
        url = reverse("api_participant_list", kwargs={"p_type": self.kwargs["p_type"]})
        params = urllib.parse.urlencode(info_filter.as_get_params())
        return HttpResponseRedirect(url + "?%s" % params)
