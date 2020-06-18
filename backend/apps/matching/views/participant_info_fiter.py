import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from apps.matching.forms import ParticipantFilterForm

logger = logging.getLogger(__name__)


class ParticipantFilterCreateView(CreateView, LoginRequiredMixin):
    """Create a persistent Filter."""

    template_name = "participant/participant_create_form.html"
    success_url = "/matching/thanks-registration"

    def get_form_class(self):
        return ParticipantFilterForm[self.kwargs["p_type"]]

    def form_valid(self, form):
        info_filter = form.save(commit=False)
        info_filter.created_by = self.request.user
        info_filter.save()
        return HttpResponseRedirect(self.success_url)
