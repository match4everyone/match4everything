from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django_tables2 import SingleTableView

from apps.matching.models import Match, MATCH_STATE_OPTIONS
from apps.matching.tables import MatchFromOthersTable


@method_decorator([login_required], name="dispatch")
class MatchesFromOthersView(SingleTableView):
    template_name = "matches/matches_from_others_list.html"

    def get_table_class(self):
        p_type = self.request.user.participant().participant_type
        return MatchFromOthersTable[p_type]

    def get_queryset(self):
        p_type = self.request.user.participant().participant_type
        if p_type == "A":
            return Match.objects.filter(participantA=self.request.user.participant(), initiator="B")
        else:
            return Match.objects.filter(participantB=self.request.user.participant(), initiator="A")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_type = self.request.user.participant().participant_type
        context["p_type"] = p_type
        return context

    def post(self, request):
        match = get_object_or_404(Match, uuid=request.POST["uuid"])

        if "interested" in request.POST:
            match.state = MATCH_STATE_OPTIONS.SUCCESSFUL
            match.save()
            return HttpResponseRedirect(reverse("matches-requests-to-me"))
        elif "block" in request.POST:
            match.state = MATCH_STATE_OPTIONS.BLOCKED
            match.save()
            return HttpResponseRedirect(reverse("matches-requests-to-me"))
        raise Http404
