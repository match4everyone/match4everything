import django_tables2 as tables

from apps.matching.models import ParticipantInfoFilter
from apps.matching.src.dual_factory import instanciate_for_participants


def make_filter_tables(p_type):
    class FilterTable(tables.Table):
        matches = tables.Column(empty_values=())
        name = tables.TemplateColumn(
            template_name="filters/table_name_col.html", extra_context={"p_type": p_type}
        )

        class Meta:
            model = ParticipantInfoFilter[p_type]
            template_name = "django_tables2/bootstrap.html"
            fields = ["registration_date", "name"]

        def render_matches(self, record):
            return ParticipantInfoFilter[p_type].objects.get(id=record.id).matching_infos()

    return FilterTable


FilterTable = instanciate_for_participants(make_filter_tables)
