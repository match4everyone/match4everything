from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from apps.matching.models import ParticipantInfo
from apps.matching.src.dual_factory import instanciate_for_participants


def make_participant_edit_info_form(participant_type):
    class ParticipantEditInfoForm(forms.ModelForm):
        class Meta:
            model = ParticipantInfo[participant_type]
            exclude = ParticipantInfo[participant_type].excluded_fields()

        def __init__(self, *args, **kwargs):
            super(ParticipantEditInfoForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.add_input(
                Submit(
                    "submit",
                    "Save",
                    css_class="btn-primary",
                    onclick="this.form.submit(); this.disabled=true; this.value='Sending…';",
                )
            )

    return ParticipantEditInfoForm


ParticipantEditInfoForm = instanciate_for_participants(make_participant_edit_info_form)
