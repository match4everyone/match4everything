from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView

from apps.matching.admin import matching_participant_required
from apps.matching.forms import ParticipantEditInfoForm
from apps.matching.models import ParticipantInfo


@method_decorator([login_required, matching_participant_required], name="dispatch")
class ParticipantInfoUpdateView(UpdateView):
    """Updates the information of either participant."""

    template_name = "participant/participant_info_edit_form.html"
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
            return HttpResponseForbidden()
        return super(ParticipantInfoUpdateView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        return ParticipantEditInfoForm[self.kwargs["p_type"]]

    def get_queryset(self):
        return ParticipantInfo[self.kwargs["p_type"]].objects.all()

    def get_success_url(self):
        return reverse("profile")

    def form_valid(self, form):
        res = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, _("Successfully updated info."))
        return res
