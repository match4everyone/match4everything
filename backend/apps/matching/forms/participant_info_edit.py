from crispy_forms.helper import FormHelper
from django import forms

from apps.matching.models import ParticipantInfo
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_participant_info_edit_form(participant_type):
    class ParticipantInfoEditForm(forms.ModelForm):
        class Meta:
            model = ParticipantInfo[participant_type]
            exclude = ParticipantInfo[participant_type].excluded_fields()

        def __init__(self, *args, **kwargs):
            super(ParticipantInfoEditForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False

    return ParticipantInfoEditForm


ParticipantInfoEditForm = instanciate_for_participants(make_participant_info_edit_form)
