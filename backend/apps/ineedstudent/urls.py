from django.urls import path, register_converter

from apps.iamstudent.views import StudentSelectionView

from . import converters, views

register_converter(converters.DecimalPointFloatConverter, "float")


urlpatterns = [
    path(
        "students/<countrycode>/<plz>/<float:distance>",
        StudentSelectionView.as_view(),
        name="list_by_plz",
    ),
    path("hospitals/<countrycode>/<plz>", views.HospitalListView.as_view(), name="hospital_list"),
    path("hospital_map", views.HospitalMapView.as_view(), name="hopsital_map"),
    path("zustimmung", views.HospitalDataConsent.as_view(), name="zustimmung"),
    path("hospital_view/<str:uuid>/", views.HospitalDetailView.as_view(), name="hospital_view"),
    path("hospital_dashboard", views.HospitalDashboardView.as_view(), name="hospital_dashboard"),
    path("change_posting", views.HospitalPostingEditView.as_view(), name="change_posting"),
]
