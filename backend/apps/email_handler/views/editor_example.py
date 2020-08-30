import uuid
import html2text

from django.urls import reverse, reverse_lazy
from django.utils.text import format_lazy
from django.utils.translation import gettext as _
from django.views.generic import FormView

from apps.email_handler.forms import TemplateEditorForm
from post_office.models import EmailTemplate


class MailEditor(FormView):
    form_class = TemplateEditorForm
    template_name = "mail_editor.html"
    success_url = reverse_lazy("mails_sent_successfully")

    def get_initial(self):
        initial = super(MailEditor, self).get_initial()
        # ToDo load initial from template or have selector which does?
        subject = _("Ein Ort braucht Deine Hilfe")
        html_content = format_lazy(
            _(
                """
                <p>Liebe(r) Helfende(r),</p>
                
                <p>Wir sind...<br />
                Wir suchen...<br />
                Meldet euch baldm&ouml;glichst!</p>
                
                <p>Beste Gr&uuml;&szlig;e,<br />
                Name Ansprechpartner<br />
                Tel:<br />
                Email:</p>
                """
            ),
        )
        initial.update({"subject": subject, "html_content": html_content})
        return initial

    def form_valid(self, form):
        # --- Generate new uuid and save as name
        new_uuid = str(uuid.uuid4())
        for __ in range(42):
            if not EmailTemplate.objects.filter(name__exact=new_uuid):
                break
            new_uuid = str(uuid.uuid4())

        # --- Save template
        mail_template = form.save(commit=False)

        # ToDo sanitize / bleach input
        # ToDo make template extend from base mail template

        # Convert html content to pain text
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = False
        mail_template.content = text_maker.handle(mail_template.html_content)
        mail_template.name = new_uuid
        mail_template.save()
        return super().form_valid(form)
