from django.http import HttpResponseRedirect
from django.urls import reverse
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from apps.matching.models import (
    Match,
    ParticipantInfo,
    ParticipantInfoFilter,
    ParticipantInfoFilterSet,
)
from apps.matching.tables import ParticipantInfoTable

# block other person table
# match - a,b,contact_request,filter, state = blocked
# filter - stateful mit text ('einen ähnliche Suche nochmal starten')


class FilteredParticipantList(SingleTableMixin, FilterView):

    template_name = "participant/participant_filtered.html"

    # @transaction.atomic
    def post(self, request, p_type):
        """SELECT A selection of participants was received."""
        uuids = request.POST.getlist("uuid")
        filtered_p_type = p_type

        filterset = self.get_filterset_kwargs(self.get_filterset_class())["data"].copy()

        filter_ = ParticipantInfoFilter[p_type].create_from_filterset(
            filter_kwargs=filterset, created_by=request.user
        )
        filter_.contact_text = request.POST["msg-only-subject"]
        filter_.subject = request.POST["msg-only-contact_text"]
        filter_.save()
        # save filter before
        for uuid in uuids:
            filtered = ParticipantInfo[p_type].objects.get(uuid=uuid).participant

            if filtered_p_type == "A":
                m = Match.objects.create(
                    participantA=filtered,
                    participantB=self.request.user.participant(),
                    filterA=filter_,
                    initiator="B",
                )
                m.save()
            else:
                m = Match.objects.create(
                    participantA=self.request.user.participant(),
                    participantB=filtered,
                    filterB=filter_,
                    initiator="A",
                )
                m.save()

        return HttpResponseRedirect(reverse("profile"))

    def get_model_class(self):
        return ParticipantInfo[self.kwargs["p_type"]]

    def get_filterset_class(self):
        return ParticipantInfoFilterSet[self.kwargs["p_type"]]

    def get_table_class(self):
        return ParticipantInfoTable[self.kwargs["p_type"]]
