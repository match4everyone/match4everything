from django.urls import include, path

from django.urls import path, register_converter

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]
