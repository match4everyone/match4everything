import logging

from django.views.generic.edit import CreateView

from apps.matching.forms import ParticipantSignupForm
from apps.matching.src.notifications import send_password_set_email

logger = logging.getLogger(__name__)


class ParticipantSignup(CreateView):
    """Signup a participant."""

    template_name = "participant/participant_create_form.html"
    success_url = "/matching/thanks-registration"
    subject_template = "registration/password_reset_email_subject.txt"
    mail_template = "registration/password_set_email.html"

    def get_form_class(self):
        return ParticipantSignupForm[self.kwargs["p_type"]]

    def form_valid(self, form):
        response = super(ParticipantSignup, self).form_valid(form)
        send_password_set_email(
            email=self.object.user.email,
            host=self.request.META["HTTP_HOST"],
            subject_template=self.subject_template,
            template=self.mail_template,
        )
        return response
