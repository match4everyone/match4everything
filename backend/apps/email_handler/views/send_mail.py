import time

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView


class SendMailView(TemplateView):
    template_name = "emails_sent.html"

    def post(self, request, **kwargs):
        time.sleep(1)
        return JsonResponse(request.POST)
