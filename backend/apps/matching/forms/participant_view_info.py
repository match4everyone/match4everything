from crispy_forms.helper import FormHelper
from django import forms

from apps.matching.models import ParticipantInfo
from apps.matching.src.dual_factory import instanciate_for_participants


def make_participant_view_info_form(participant_type):
    class ParticipantViewInfoForm(forms.ModelForm):
        class Meta:
            model = ParticipantInfo[participant_type]
            exclude = ParticipantInfo[participant_type].private_fields()

        def __init__(self, *args, **kwargs):
            super(ParticipantViewInfoForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            for field in self.fields:
                self.fields[field].disabled = True

            self._hide_dropdown = (
                "-webkit-appearance:none;-moz-appearance:none;text-indent:1px;text-overflow:'';"
            )

    return ParticipantViewInfoForm


ParticipantViewInfoForm = instanciate_for_participants(make_participant_view_info_form)
