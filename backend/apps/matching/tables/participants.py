import django_tables2 as tables

from apps.matching.models import ParticipantInfo
from apps.matching.src.dual_factory import instanciate_for_participants


def make_participant_info_tables(p_type):
    class ParticipantInfoTable(tables.Table):

        uuid = tables.CheckBoxColumn()

        class Meta:
            model = ParticipantInfo[p_type]
            template_name = "django_tables2/bootstrap.html"
            fields = ["registration_date", "participant__user__email"]

    return ParticipantInfoTable


ParticipantInfoTable = instanciate_for_participants(make_participant_info_tables)
