from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import Http404

from apps.matching.models import CountryCodeChoices, RadiusChoices


def view_FilterOptionsJSON(request, p_type):

    if p_type == "A":
        filter_options = settings.PARTICIPANT_SETTINGS["A"].to_filter_json()
    elif p_type == "B":
        filter_options = settings.PARTICIPANT_SETTINGS["B"].to_filter_json()
    else:
        raise Http404

    filter_options["location"] = {
        "location_distance": RadiusChoices.choices,
        "location_country_code": CountryCodeChoices.choices,
    }

    return JsonResponse(filter_options)
