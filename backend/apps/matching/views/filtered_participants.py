from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from apps.matching.models import ParticipantInfo, ParticipantInfoFilterSet
from apps.matching.tables import ParticipantInfoTable


class FilteredParticipantList(SingleTableMixin, FilterView):

    template_name = "participant/participant_filtered.html"

    def get_model_class(self):
        return ParticipantInfo[self.kwargs["p_type"]]

    def get_filterset_class(self):
        return ParticipantInfoFilterSet[self.kwargs["p_type"]]

    def get_table_class(self):
        return ParticipantInfoTable[self.kwargs["p_type"]]
