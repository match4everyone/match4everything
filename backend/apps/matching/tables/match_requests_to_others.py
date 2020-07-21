from django.utils.translation import gettext as _
import django_tables2 as tables
from django_tables2 import Column, TemplateColumn

from apps.matching.models import Match
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_matches_to_others(p_type):
    class MatchToOthersTable(tables.Table):
        info = TemplateColumn(
            accessor="email_receiver_url",
            template_name="matches/profile_view_requested_col.html",
            verbose_name=_("Contact"),
        )
        mail = Column(accessor="email_receiver", verbose_name=_("Email"))
        message = TemplateColumn(
            accessor="inital_message",
            template_name="filters/mail_of_match_no_reply_col.html",
            verbose_name=_("Your message"),
        )
        filter_ = TemplateColumn(
            template_code='<a class="link" href="{{value}}">view search</a>',
            accessor="filter_url",
            verbose_name=_("Match criteria"),
        )

        class Meta:
            model = Match
            template_name = "django_tables2/bootstrap4.html"
            fields = []

    return MatchToOthersTable


MatchToOthersTable = instanciate_for_participants(make_matches_to_others)
