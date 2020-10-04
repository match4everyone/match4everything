from django.http import JsonResponse
from django.shortcuts import Http404

from match4everyone.configuration.A import A
from match4everyone.configuration.B import B


def view_TableColumnJSON(request, p_type):

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
