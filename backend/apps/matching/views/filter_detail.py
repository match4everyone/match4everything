from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from apps.matching.models import Match, ParticipantInfoFilter


@method_decorator([login_required], name="dispatch")
class FilterDetailView(DetailView):

    template_name = "filters/filter_detail.html"

    def get_model_class(self):
        return ParticipantInfoFilter[self.kwargs["p_type"]]

    def dispatch(self, request, *args, **kwargs):

        # check if user is involved in a match via the filter or owns it
        filter_ = self.get_object()
        if self.kwargs["p_type"] == "A":
            matches = Match.objects.filter(filterA=filter_)
        else:
            matches = Match.objects.filter(filterB=filter_)

        user_p_type = self.request.user.participant().participant_type
        if user_p_type == "A":

            is_in_touch_via_filter = (
                matches.filter(participantA=self.request.user.participant()).count() > 0
            )
        else:
            is_in_touch_via_filter = (
                matches.filter(participantB=self.request.user.participant()).count() > 0
            )

        if filter_.created_by == self.request.user or is_in_touch_via_filter:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404

    def get_object(self, queryset=None):
        return get_object_or_404(
            ParticipantInfoFilter[self.kwargs["p_type"]], uuid=self.kwargs["uuid"]
        )
