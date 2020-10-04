from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, metadata, serializers

from apps.matching.models import ParticipantInfo, ParticipantInfoFilterSet


class FilterBackend(DjangoFilterBackend):
    """FilterBackend for getting a list of participants."""

    def get_filterset_class(self, view, queryset=None):
        if hasattr(view, "get_filterset_class"):
            return view.get_filterset_class()
        return view.filterset_class


class FilterMetadata(metadata.BaseMetadata):
    """Provide metadata if the endpoint is called with the OPTIONS header."""

    def determine_metadata(self, request, view):
        p_type = view.kwargs["p_type"]
        filter_specification = ParticipantInfoFilterSet[p_type].filter_spec()

        return {
            "name": view.get_view_name(),
            "description": view.get_view_description(),
            "actions": {"GET": filter_specification},
        }


# how do we want to manage access here? Only let users be searchable for each other?
@method_decorator([login_required], name="dispatch")
class ParticipantInfoListAPI(generics.ListAPIView):
    filter_backends = (FilterBackend,)
    metadata_class = FilterMetadata

    def get_serializer_class(self):
        class Serializer(serializers.ModelSerializer):
            class Meta:
                model = ParticipantInfo[self.kwargs["p_type"]]
                exclude = [f for f in model.private_fields() if f != "uuid"]

        return Serializer

    def get_queryset(self):
        return ParticipantInfo[self.kwargs["p_type"]].objects.all()

    def get_filterset_class(self):
        return ParticipantInfoFilterSet[self.kwargs["p_type"]]
