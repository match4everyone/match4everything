from django.template.loader import get_template
import django_tables2 as tables
from django_tables2 import Column, TemplateColumn

from apps.matching.models import Match, MATCH_STATE_OPTIONS
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_matches_from_others(p_type):
    class MatchFromOthersTable(tables.Table):
        mail = Column(accessor="email_initiator", empty_values=(), verbose_name="E-Mail")
        mail_info = TemplateColumn(
            accessor="email_initiator_url",
            verbose_name="",
            empty_values=(),
            template_code='<a href="{{value}}"><i class="fa fa-info-circle" aria-hidden="true"></i></a>',
        )
        message = TemplateColumn(
            accessor="inital_message",
            template_name="filters/mail_of_match_col.html",
            verbose_name="Contact Request",
        )
        state = Column(accessor="state", empty_values=(), verbose_name="")
        filter_ = TemplateColumn(
            template_code='<a class="link" href="{{value}}">view filter</a>',
            accessor="filter_url",
            verbose_name="Match criteria",
        )

        class Meta:
            model = Match
            template_name = "django_tables2/bootstrap4.html"
            fields = []

        def render_state(self, record):
            context = {"options": MATCH_STATE_OPTIONS, "value": record.state, "uuid": record.uuid}
            return get_template("matches/response_options.html").render(
                context, request=self.request
            )

    return MatchFromOthersTable


MatchFromOthersTable = instanciate_for_participants(make_matches_from_others)
