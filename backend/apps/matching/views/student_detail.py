import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.matching.admin import hospital_required
from apps.matching.forms import StudentFormView
from apps.matching.models import Student

logger = logging.getLogger(__name__)


@method_decorator([login_required, hospital_required], name="dispatch")
class StudentDetailView(View):
    def get(self, request, uuid):
        s = Student.objects.get(uuid=uuid)
        form = StudentFormView(instance=s, prefix="infos")
        context = {"form": form}
        return render(request, "view_student.html", context)
