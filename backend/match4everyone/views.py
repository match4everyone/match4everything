from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.template import loader


def home(request):
    context = {}
    template = loader.get_template("home.html")

    return HttpResponse(template.render(context, request))


def about(request):

    context = {}
    template = loader.get_template("about.html")

    return HttpResponse(template.render(context, request))


def impressum(request):
    context = {}
    template = loader.get_template("impressum.html")

    return HttpResponse(template.render(context, request))


def dataprotection(request):
    context = {}
    template = loader.get_template("dataprotection.html")

    return HttpResponse(template.render(context, request))


def legal_questions(request):
    context = {}
    template = loader.get_template("legal-questions.html")

    return HttpResponse(template.render(context, request))


def terms_of_use(request):
    context = {}
    template = loader.get_template("terms-of-use.html")

    return HttpResponse(template.render(context, request))


def handler403(request, exception=None):
    template = loader.get_template("403.html")
    return HttpResponseForbidden(template.render({}, request))


def handler404(request, exception=None):
    template = loader.get_template("404.html")
    return HttpResponseNotFound(template.render({}, request))


def handler500(request):
    template = loader.get_template("500.html")
    return HttpResponseServerError(template.render({}, request))
