from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, HTML, Layout, Row
from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.matching.models import Participant, ParticipantInfo, User
from apps.matching.utils.dual_factory import instanciate_for_participants
from match4everyone.configuration.A import A
from match4everyone.configuration.B import B


def make_participant_signup_form(participant_type):
    class ParticipantSignupForm(forms.ModelForm):

        # add more query fields
        email = forms.EmailField(
            validators=[User.validate_email_not_taken], label=_("Email address for your account."),
        )

        class Meta:
            model = ParticipantInfo[participant_type]
            exclude = ParticipantInfo[participant_type].excluded_fields()

        def __init__(self, *args, **kwargs):
            super(ParticipantSignupForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            if participant_type == "A":
                self.helper.layout = Layout(
                    Div(Div(Row(Column("email")), css_class="card-body"), css_class="card"),
                    HTML("<br>"),
                    *A.get_signup_layout()
                )
            else:
                self.helper.layout = Layout(
                    Div(Div(Row(Column("email")), css_class="card-body"), css_class="card"),
                    HTML("<br>"),
                    *B.get_signup_layout()
                )

        @transaction.atomic
        def save(self):
            p = Participant[participant_type].new(participant_type, self.cleaned_data["email"])
            i = ParticipantInfo[participant_type].objects.create(
                participant=p, **{k: i for k, i in self.cleaned_data.items() if k != "email"}
            )
            i.save()
            return p, i

        def is_valid(self):
            return super().is_valid()

    return ParticipantSignupForm


ParticipantInfoSignupForm = instanciate_for_participants(make_participant_signup_form)
