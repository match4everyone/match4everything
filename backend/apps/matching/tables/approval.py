import django_tables2 as tables
from django_tables2 import TemplateColumn

from apps.matching.models import Participant
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_staff_approvals_table(p_type):
    class ApproveParticipantTable(tables.Table):
        info = TemplateColumn(
            template_name="staff/user_info_button.html",
            extra_context={"p_type": p_type},
            accessor="info_uuid",
        )
        status = TemplateColumn(template_name="staff/approval_button.html")
        delete = TemplateColumn(template_name="staff/delete_button.html")

        class Meta:
            model = Participant[p_type]
            template_name = "django_tables2/bootstrap4.html"
            fields = ["user__email"]

    return ApproveParticipantTable


ApproveParticipantTable = instanciate_for_participants(make_staff_approvals_table)
