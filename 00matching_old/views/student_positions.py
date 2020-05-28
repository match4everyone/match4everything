from django.http import JsonResponse

from apps.matching_old.models import Student
from apps.matching_old.src.map import group_by_zip_code


def supportersJSON(request):
    students = Student.objects.filter(user__validated_email=True)
    supporters = group_by_zip_code(students)
    return JsonResponse(supporters)
