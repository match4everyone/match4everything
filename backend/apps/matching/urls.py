from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path, register_converter
from django.views.generic.base import TemplateView

from . import views
from .utils import converters

register_converter(converters.DecimalPointFloatConverter, "float")
register_converter(converters.ParticipantTypeConverter, "p")

urlpatterns = [
    ####################################
    #  User signup/editing/dashboards
    ####################################
    path("<p:p_type>/signup/", views.ParticipantSignup.as_view(), name="signup"),
    path("profile_redirect/", views.ProfileDashboardRedirect.as_view(), name="profile_redirect",),
    path("profile/", views.ParticipantDashboard.as_view(), name="profile"),
    path(
        "<p:p_type>/info/<str:uuid>/edit/",
        views.ParticipantInfoUpdateView.as_view(),
        name="info-edit",
    ),
    path(
        "<p:p_type>/info/<str:uuid>/view/",
        views.ParticipantInfoViewView.as_view(),
        name="info-view",
    ),
    path("matches/to_me/", views.MatchesFromOthersView.as_view(), name="matches-requests-to-me",),
    path("matches/from_me/", views.MatchesToOthersView.as_view(), name="matches-requests-from-me",),
    path(
        "change_activation/",
        views.ChangeActivationAskView.as_view(),
        name="activate_participant_ask",
    ),
    path(
        "change_activation_confirm/",
        views.ChangeActivationRedirect.as_view(),
        name="activate_participant",
    ),
    path("delete_me_ask/", views.delete_me_ask, name="delete_me_ask"),
    path("delete_me/", views.delete_me, name="delete_me"),
    ####################################
    #  Map view
    ####################################
    path("map/", views.map_view, name="map"),
    path("<p:p_type>/participant_JSON/", views.map_JSON, name="participant_JSON"),
    ####################################
    #  List view / filtering
    ####################################
    path(
        "api/<p:p_type>/info/list/",
        views.ParticipantInfoListAPI.as_view(),
        name="api_participant_list",
    ),
    path("<p:p_type>/", views.FilteredParticipantList.as_view(), name="participant_list",),
    path(
        "<p:p_type>/filter/create/",
        views.ParticipantFilterCreateView.as_view(),
        name="create_participant_filter",
    ),
    path(
        "<p:p_type>/filter/<str:uuid>/view/", views.FilterDetailView.as_view(), name="filter_detail"
    ),
    path(
        "<p:p_type>/filter/<str:uuid>/search_again/",
        views.ParticipantFilterSearchAgain.as_view(),
        name="filter_search_again",
    ),
    path(
        "<p:p_type>/filter/<str:uuid>/contact_new_matches/",
        views.FilterContactNewMatchView.as_view(),
        name="contact_all_new_matches",
    ),
    path(
        "<p:p_type>/filter/<str:uuid>/edit/", views.FilterUpdateView.as_view(), name="filter-edit",
    ),
    path("<p:p_type>/filter/list/", views.FilterListView.as_view(), name="filter_list"),
    ####################################
    #  Staff
    ####################################
    path("staff_profile/", views.StaffProfileView.as_view(), name="staff_profile"),
    path(
        "staff/<p:p_type>/approve/",
        views.ApproveParticipantsView.as_view(),
        name="approve_participant",
    ),
    path("staff/<p:p_type>/mail_limit", views.IncreaseMailLimitView.as_view(), name="mail_limit",),
    ####################################
    #  Authentication
    ####################################
    path(
        "thanks-registration/",
        TemplateView.as_view(template_name="messages/thanks_for_registering.html"),
        name="thanks-registration",
    ),
    path("login_redirect/", views.LoginRedirect.as_view(), name="login_redirect"),
    path("validate_email/", views.validate_email, name="validate_email"),
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
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form_.html"
        ),
        name="password_change_form",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form_.html",
            from_email=settings.NOREPLY_MAIL,
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
            success_url="/matching/validate_email/",
        ),
        name="password_reset_confirm_",
    ),
    path(
        "resend_validation_email/<email>/",
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
