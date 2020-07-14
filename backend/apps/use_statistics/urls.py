from django.urls import path

from . import views

app_name = "use_statistics"
urlpatterns = [
    path("view", views.use_statistics, name="view"),
]
