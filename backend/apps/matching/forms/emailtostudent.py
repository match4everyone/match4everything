from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, HTML, Layout, Row, Submit

from apps.matching.models import EmailToSend


class EmailToSendForm(forms.ModelForm):
    class Meta:
        model = EmailToSend
        fields = ["subject", "message"]
        labels = {"subject": _("Betreff"), "message": _("Nachrichtentext")}
        help_texts = {}

    def clean_message(self):
        message = self.cleaned_data["message"]
        initial_message = self.initial["message"]
        if "".join(str(message).split()) == "".join(str(initial_message).split()):
            raise ValidationError(_("Bitte personalisiere diesen Text"), code="invalid")
        return message

    def __init__(self, *args, **kwargs):
        super(EmailToSendForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            HTML("<h2 class='form-heading'>{}</h2>".format(_("Persönliche Informationen"))),
            "subject",
            Div(
                HTML(
                    _(
                        "Bitte schreiben Sie in diese Mail an die Helfenden kurze Informationen zur geplanten Tätigkeit:\n\n"
                        "<ul>"
                        "<li>zeitlicher Umfang,</li>"
                        "<li>Aufgabengebiet/Abteilung</li>"
                        "<li>Vergütung / Modalitäten</li>"
                        "<li>Arbeitsvertrag / Versicherungsverhältnis</li></ul>"
                        "So können die Helfenden schneller sehen, ob diese Stelle zu Ihnen passt, sparen sich "
                        "Nachfragen bei Ihnen und können zügiger zu- oder absagen.\n\n"
                    )
                ),
                HTML(
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'
                    '<span aria-hidden="true">&times;</span>'
                    "</button>"
                ),
                css_class="alert alert-info alert-dismissable",
                role="alert",
            ),
            "message",
        )
