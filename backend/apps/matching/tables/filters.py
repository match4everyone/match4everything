from django.utils.translation import gettext as _
import django_tables2 as tables

from apps.matching.models import Match, ParticipantInfoFilter
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_filter_tables(p_type):
    class FilterTable(tables.Table):
        registration_date = tables.Column(accessor="registration_date", verbose_name=_("Created"))
        filter_name = tables.TemplateColumn(
            template_name="matches/col-edit_search_name.html",
            extra_context={"p_type": p_type},
            verbose_name=_("Name"),
        )
        matches = tables.Column(empty_values=(), verbose_name=_("New matches"))
        new_matches_you_did_not_contact = tables.TemplateColumn(
            template_name="matches/col-contact_new_match.html", verbose_name="", empty_values=()
        )
        search_again = tables.TemplateColumn(
            template_name="matches/col-search_again.html",
            verbose_name="",
            extra_context={"p_type": p_type},
        )

        class Meta:
            model = ParticipantInfoFilter[p_type]
            template_name = "django_tables2/bootstrap.html"
            fields = []

        def render_matches(self, record):
            filter_ = ParticipantInfoFilter[p_type].objects.get(id=record.id)
            (
                already_in_contact_with,
                already_contacted_with_via_filter,
                available_matches,
            ) = Match.matches_to(filter_)

            return f"{available_matches - already_in_contact_with}"

    return FilterTable


FilterTable = instanciate_for_participants(make_filter_tables)
