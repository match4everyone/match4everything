from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_tables2 import SingleTableView

from apps.matching.models import ParticipantInfoFilter
from apps.matching.tables import FilterTable


@method_decorator([login_required], name="dispatch")
class FilterListView(SingleTableView):
    template_name = "filters/filter_list.html"

    def get_table_class(self):
        return FilterTable[self.kwargs["p_type"]]

    def get_queryset(self):
        return ParticipantInfoFilter[self.kwargs["p_type"]].objects.filter(
            created_by=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["p_type"] = self.kwargs["p_type"]
        return context
