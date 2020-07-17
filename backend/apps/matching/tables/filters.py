import django_tables2 as tables

from apps.matching.models import Match, ParticipantInfoFilter
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_filter_tables(p_type):
    class FilterTable(tables.Table):
        matches = tables.Column(
            empty_values=(), verbose_name="(inContactWith,inContactViaFilter,Matches)"
        )
        filter_name = tables.TemplateColumn(
            template_name="filters/table_name_col.html", extra_context={"p_type": p_type}
        )
        new_matches_you_did_not_contact = tables.TemplateColumn(
            template_name="filters/contact_new_match_col.html", verbose_name="", empty_values=()
        )
        search_again = tables.Column(empty_values=())

        class Meta:
            model = ParticipantInfoFilter[p_type]
            template_name = "django_tables2/bootstrap.html"
            fields = ["registration_date"]

        def render_matches(self, record):
            filter_ = ParticipantInfoFilter[p_type].objects.get(id=record.id)
            matches = Match.matches_to(filter_)
            return matches

        def render_search_again(self, record):
            return "(button: search again)"

    return FilterTable


FilterTable = instanciate_for_participants(make_filter_tables)
