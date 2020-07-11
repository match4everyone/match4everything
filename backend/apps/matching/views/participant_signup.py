import logging

from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from apps.matching.admin import logged_in_not_permitted
from apps.matching.forms import ParticipantInfoSignupForm
from apps.matching.models import ParticipantInfoLocation
from apps.matching.utils.notifications import send_password_set_email

logger = logging.getLogger(__name__)


@method_decorator(logged_in_not_permitted, name="dispatch")
class ParticipantSignup(View):
    """Signup a participant."""

    # inspired by : https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0
    template_name = "participant/participant_create_form.html"
    success_url = "/matching/thanks-registration"
    subject_template = "registration/password_reset_email_subject.txt"
    mail_template = "registration/password_set_email.html"

    def get_form_class(self):
        return ParticipantInfoSignupForm[self.kwargs["p_type"]]

    def get(self, request, p_type):
        LocationFormSet = modelformset_factory(
            ParticipantInfoLocation[p_type],
            exclude=ParticipantInfoLocation[p_type].excluded_fields(),
            extra=1,
        )

        context = {}
        context["location_formset"] = LocationFormSet(
            queryset=ParticipantInfoLocation[self.kwargs["p_type"]].objects.none(),
            prefix="location",
        )
        context["info_form"] = ParticipantInfoSignupForm[self.kwargs["p_type"]](prefix="info")
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        LocationFormSet = modelformset_factory(
            ParticipantInfoLocation[self.kwargs["p_type"]],
            exclude=ParticipantInfoLocation[self.kwargs["p_type"]].excluded_fields(),
            extra=1,
        )
        location_formset = LocationFormSet(request.POST, prefix="location")
        info_form = ParticipantInfoSignupForm[self.kwargs["p_type"]](
            data=request.POST, prefix="info"
        )
        if location_formset.is_valid() and info_form.is_valid():
            return self.form_valid(location_formset, info_form)
        return render(
            request,
            self.template_name,
            {"location_formset": location_formset, "info_form": info_form,},
        )

    def form_valid(self, location_formset, info_form):
        participant, info = info_form.save()
        instances = location_formset.save(commit=False)
        for inst in instances:
            inst.participant_info = info
            inst.save()

        send_password_set_email(
            email=participant.user.email,
            host=self.request.META["HTTP_HOST"],
            subject_template=self.subject_template,
            template=self.mail_template,
        )
        return HttpResponseRedirect(self.success_url)
