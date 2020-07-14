import django_tables2 as tables
from django_tables2 import TemplateColumn

from apps.matching.models import Participant
from apps.matching.utils.dual_factory import instanciate_for_participants

mail_limit_field = (
    "<form>{% csrf_token %}"
    '<input type="hidden" value="{{record.uuid}}" name="uuid"> '
    '<input type="number" value="{{record.max_mails_per_day}}" step="1" pattern="\d+" class="btn btn-sm" name="mail_limit" onClick="this.select();" />'
    '<button type="submit" formmethod="post" class="btn btn-sm btn-success">'
    "Submit"
    "</button>"
    "</form>"
)  # noqa


def make_mail_limits_table(p_type):
    class MailLimitsTable(tables.Table):
        info = TemplateColumn(
            template_name="staff/user_info_button.html", extra_context={"p_type": p_type}
        )
        mail_limit_field = TemplateColumn(template_code=mail_limit_field)

        class Meta:
            model = Participant[p_type]
            template_name = "django_tables2/bootstrap4.html"
            fields = ["user__email"]

    return MailLimitsTable


MailLimitsTable = instanciate_for_participants(make_mail_limits_table)
