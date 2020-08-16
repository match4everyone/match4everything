import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from apps.matching.forms import ParticipantInfoEditForm
from apps.matching.models import ParticipantInfo, ParticipantInfoLocation

logger = logging.getLogger(__name__)


@method_decorator([login_required], name="dispatch")
class ParticipantInfoUpdateView(View):
    """Edit a profile."""

    template_name = "participant/participant_info_edit_form.html"
    success_url = reverse_lazy("profile")

    def dispatch(self, *args, **kwargs):
        user_from_url = get_object_or_404(
            ParticipantInfo[self.kwargs["p_type"]], uuid=kwargs["uuid"]
        ).participant.user
        user_from_request = self.request.user
        if user_from_request != user_from_url:
            raise PermissionDenied
        return super(ParticipantInfoUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, p_type, uuid):
        info = get_object_or_404(ParticipantInfo[p_type], uuid=uuid)

        LocationFormSet = inlineformset_factory(
            ParticipantInfo[p_type],
            ParticipantInfoLocation[p_type],
            exclude=ParticipantInfoLocation[p_type].excluded_fields(),
            can_delete=True,
            extra=0,
        )

        context = {}
        context["location_formset"] = LocationFormSet(instance=info, prefix="location")
        context["info_form"] = ParticipantInfoEditForm[p_type](prefix="info", instance=info)

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, p_type, uuid):
        info = get_object_or_404(ParticipantInfo[p_type], uuid=uuid)
        LocationFormSet = inlineformset_factory(
            ParticipantInfo[p_type],
            ParticipantInfoLocation[p_type],
            exclude=ParticipantInfoLocation[p_type].excluded_fields(),
        )
        location_formset = LocationFormSet(request.POST, instance=info, prefix="location")
        info_form = ParticipantInfoEditForm[self.kwargs["p_type"]](
            data=request.POST, prefix="info", instance=info
        )
        if location_formset.is_valid() and info_form.is_valid():
            info_form.save()
            location_formset.save()
            messages.add_message(self.request, messages.INFO, _("Successfully updated info."))
            return HttpResponseRedirect(self.success_url)
        messages.add_message(
            self.request, messages.ERROR, _("Oh no, there were some errors in the form below.")
        )
        return render(
            request,
            self.template_name,
            {"location_formset": location_formset, "info_form": info_form,},
        )
