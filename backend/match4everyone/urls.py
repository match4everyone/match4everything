"""match4everyone URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import re_path
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

from match4everyone import views

urlpatterns = [
    path("matching/", include("apps.matching.urls")),
    path("use_statistics/", include("apps.use_statistics.urls")),
    path("django-administration/", admin.site.urls),
    path("403/", views.handler403, name="403"),
    path("404/", views.handler404, name="404"),
    path("500/", views.handler500, name="500"),
    path("legal-questions/", views.legal_questions),
    path(
        "jsi18n/", JavaScriptCatalog.as_view(packages=["apps.matching"]), name="javascript-catalog"
    ),
    re_path(r"^", include("cms.urls")),
]
