import django_tables2 as tables

from apps.matching.models import ParticipantInfo
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_participant_info_tables(p_type):
    class ParticipantInfoTable(tables.Table):

        info = tables.TemplateColumn(
            template_name="staff/user_info_button.html", extra_context={"p_type": p_type}
        )
        uuid = tables.CheckBoxColumn(attrs={"th": {"id": "select_all"}})

        class Meta:
            model = ParticipantInfo[p_type]
            template_name = "django_tables2/bootstrap.html"
            fields = ["registration_date"]

    return ParticipantInfoTable


ParticipantInfoTable = instanciate_for_participants(make_participant_info_tables)
