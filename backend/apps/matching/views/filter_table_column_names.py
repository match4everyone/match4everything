from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import Http404


def view_TableColumnJSON(request, p_type):

    A = settings.PARTICIPANT_SETTINGS["A"]
    B = settings.PARTICIPANT_SETTINGS["B"]

    if p_type == "A":
        names = A.get_model_field_names()
        labels = A.get_labels()
    elif p_type == "B":
        names = B.get_model_field_names()
        labels = B.gett_labels()
    else:
        raise Http404

    label_dict = {name: label for name, label in zip(names, labels)}

    return JsonResponse(label_dict)
