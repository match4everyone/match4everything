import django_tables2 as tables
from django_tables2 import Column, TemplateColumn

from apps.matching.models import Match
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_matches_to_others(p_type):
    class MatchToOthersTable(tables.Table):
        info = TemplateColumn(
            template_name="staff/user_info_button.html", extra_context={"p_type": p_type}
        )  # wont work
        mail = Column(accessor="email_receiver", verbose_name="Email")
        message = TemplateColumn(
            accessor="inital_message",
            template_name="filters/mail_of_match_col.html",
            verbose_name="inital_message_you_sent",
        )
        filter_ = TemplateColumn(
            template_code='<a class="link" href="{{value}}">view filter</a>',
            accessor="filter_url",
            verbose_name="show criteria that lead to match",
        )

        class Meta:
            model = Match
            template_name = "django_tables2/bootstrap4.html"
            fields = []

    return MatchToOthersTable


MatchToOthersTable = instanciate_for_participants(make_matches_to_others)
