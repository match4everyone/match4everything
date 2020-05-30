from django.urls import include, path
from django.conf import settings

from django.urls import path, register_converter
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from .src import converters
from . import views

register_converter(converters.DecimalPointFloatConverter, "float")
register_converter(converters.ParticipantTypeConverter, "p")

urlpatterns = [
    ####################################
    #  User signup/editing/dashboards
    ####################################
    path(
        "<p:p_type>/signup",
        views.ParticipantSignup.as_view(),
        name="signup"),
    path("profile_redirect", views.ProfileDashboardRedirect.as_view(), name="profile_redirect"),
    path("<p:p_type>/profile", views.ParticipantDashboard.as_view(), name="profile"),
    path('<p:p_type>/info/<str:uuid>/edit/$', views.ParticipantInfoUpdateView.as_view(), name='info-edit'),
    path("change_activation", views.ChangeActivationAskView.as_view(), name="activate_participant_ask"),
    path(
        "change_activation_confirm",
        views.ChangeActivationRedirect.as_view(),
        name="activate_participant",
    ),
    path("delete_me_ask", views.delete_me_ask, name="delete_me_ask"),
    path("delete_me", views.delete_me, name="delete_me"),

    ####################################
    #  Map view
    ####################################
    path("map", views.map, name="map"),
    path("<p:p_type>/participant_JSON", views.map_JSON, name="participant_JSON"),

    ####################################
    #  List view
    ####################################
    path(
        "<p:p_type>/<countrycode>/<plz>/<float:distance>",
        TemplateView.as_view(template_name='messages/not_implemented.html'),
        name="participant_list",
    ),

    ####################################
    #  Authentication
    ####################################
    path("thanks-registration", TemplateView.as_view(template_name="messages/thanks_for_registering.html"),
         name="thanks-register"),
    path("login_redirect", views.LoginRedirect.as_view(), name="login_redirect"),
    path("validate_email", views.validate_email, name="validate_email"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done_.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_change",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form_.html"
        ),
        name="password_change_form",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form_.html",
            from_email=settings.NOREPLY_MAIL
        ),
        name="password_reset_form",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done_.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete_.html"
        ),
        name="password_reset_complete_",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm_.html",
            post_reset_login=True,
            success_url="/matching/validate_email",
        ),
        name="password_reset_confirm_",
    ),
    path(
        "resend_validation_email/<email>",
        views.resend_validation_email,
        name="resend_validation_email",
    ),
    path(
        "login/",
        views.CustomLoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("", include("django.contrib.auth.urls")),
    # language
    path("i18n/", include("django.conf.urls.i18n")),
]
