from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.conf import settings

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
            if participant_type == "A":
                self.helper.layout = Layout(
                    *settings.PARTICIPANT_SETTINGS["A"].signup_and_edit_layout()
                )
            else:
                self.helper.layout = Layout(
                    *settings.PARTICIPANT_SETTINGS["B"].signup_and_edit_layout()
                )

    return ParticipantInfoEditForm


ParticipantInfoEditForm = instanciate_for_participants(make_participant_info_edit_form)
