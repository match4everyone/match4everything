from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.gzip import gzip_page

from apps.matching.models import ParticipantInfoLocation
from apps.matching.src.map import group_by_zip_code


# Should be safe against BREACH attack because we don't have user input in reponse body
@gzip_page
def map_view(request):
    template = loader.get_template("map/map.html")
    context = {"mapbox_token": settings.MAPBOX_TOKEN, "tileserver": settings.LEAFLET_TILESERVER}
    return HttpResponse(template.render(context, request))


def map_JSON(request, p_type):
    """Return the active users as a json for map use."""
    participants = ParticipantInfoLocation[p_type].objects.filter(
        participant_info__participant__user__validated_email=True,
        participant_info__participant__is_activated=True,
    )
    return JsonResponse(group_by_zip_code(participants))
