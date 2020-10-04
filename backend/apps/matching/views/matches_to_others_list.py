from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_tables2 import SingleTableView

from apps.matching.models import Match
from apps.matching.tables import MatchToOthersTable


@method_decorator([login_required], name="dispatch")
class MatchesToOthersView(SingleTableView):
    template_name = "matches/matches_to_others_list.html"

    def get_table_class(self):
        p_type = self.request.user.participant().participant_type
        return MatchToOthersTable[p_type]

    def get_queryset(self):
        p_type = self.request.user.participant().participant_type
        if p_type == "A":
            return Match.objects.filter(participantA=self.request.user.participant(), initiator="A")
        else:
            return Match.objects.filter(participantB=self.request.user.participant(), initiator="B")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_type = self.request.user.participant().participant_type
        context["p_type"] = p_type
        return context
