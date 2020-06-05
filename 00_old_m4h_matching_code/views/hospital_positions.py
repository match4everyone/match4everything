from django.http import JsonResponse

from apps.matching_old.models import Hospital
from apps.matching_old.src.map import group_by_zip_code


def facilitiesJSON(request):
    hospitals = Hospital.objects.filter(
        user__validated_email=True, is_approved=True, appears_in_map=True
    )
    facilities = group_by_zip_code(hospitals)
    return JsonResponse(facilities)
