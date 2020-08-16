from django.http import JsonResponse
from django.shortcuts import Http404

from match4everyone.configuration.A import A
from match4everyone.configuration.B import B


def view_FilterOptionsJSON(request, p_type):

    if p_type == "A":
        return JsonResponse(A().to_filter_json())
    elif p_type == "B":
        return JsonResponse(B().to_filter_json())

    raise Http404
