from crispy_forms.helper import FormHelper
from django import forms

from apps.matching.models import ParticipantInfoLocation
from apps.matching.src.dual_factory import instanciate_for_participants


def make_participant_location_form(participant_type):
    class ParticipantLocationForm(forms.ModelForm):
        class Meta:
            model = ParticipantInfoLocation[participant_type]
            exclude = ParticipantInfoLocation[participant_type].excluded_fields()

        def __init__(self, *args, **kwargs):
            super(ParticipantLocationForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False

    return ParticipantLocationForm


ParticipantLocationForm = instanciate_for_participants(make_participant_location_form)
