from django.template.loader import get_template
from django.utils.translation import gettext as _
import django_tables2 as tables
from django_tables2 import Column, TemplateColumn

from apps.matching.models import Match, MATCH_STATE_OPTIONS
from apps.matching.utils.dual_factory import instanciate_for_participants


def make_matches_from_others(p_type):
    class MatchFromOthersTable(tables.Table):
        mail = Column(accessor="email_initiator", empty_values=(), verbose_name=_("E-Mail"))
        message = TemplateColumn(
            accessor="inital_message",
            template_code="<strong>{{ value.0 }}</strong>",
            verbose_name=_("Contact Request"),
        )
        state = Column(accessor="state", empty_values=(), verbose_name="")
        view_or_respond = TemplateColumn(
            accessor="uuid", template_name="matches/col-match_detail.html", verbose_name=""
        )

        class Meta:
            model = Match
            template_name = "django_tables2/bootstrap4.html"
            fields = ["match_date"]

        def render_state(self, record):
            context = {"options": MATCH_STATE_OPTIONS, "value": record.state, "uuid": record.uuid}
            return get_template("matches/response_options.html").render(
                context, request=self.request
            )

    return MatchFromOthersTable


MatchFromOthersTable = instanciate_for_participants(make_matches_from_others)
