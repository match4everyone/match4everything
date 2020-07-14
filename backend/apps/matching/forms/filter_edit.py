from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from apps.matching.models import ParticipantInfoFilter
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_filter_edit_form(participant_type):
    class FilterEditForm(forms.ModelForm):
        class Meta:
            model = ParticipantInfoFilter[participant_type]
            exclude = ParticipantInfoFilter[participant_type].excluded_fields()

        def __init__(self, *args, **kwargs):
            super(FilterEditForm, self).__init__(*args, **kwargs)
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

    return FilterEditForm


FilterEditForm = instanciate_for_participants(make_filter_edit_form)
