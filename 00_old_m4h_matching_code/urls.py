from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.matching_old.forms import StudentForm, StudentFormAndMail
from apps.matching_old.models import Student
from apps.matching_old.forms import HospitalFormInfoCreate, HospitalFormInfoSignUp
from apps.matching_old.models import Hospital
from django.views.generic.base import TemplateView
from django.urls import path, register_converter

from apps.matching_old.views import StudentSelectionView

from . import converters

register_converter(converters.DecimalPointFloatConverter, "float")

from . import views

urlpatterns = [   path("", views.index, name="index"),
    path("facilities", views.facilitiesJSON, name="facilitiesJSON"),
    path("supporters", views.supportersJSON, name="supportersJSON"),
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
    path("thanks", TemplateView.as_view(template_name="thanks.html"), name="thanks"),
    path("successful_mail", views.EmailToStudentSuccessView.as_view(), name="success"),
    path(
        "send_mail_student/<id_list>",
        views.EmailToStudentEditView.as_view(),
        name="send_mail_student_id_list",
    ),
    path("view_student/<uuid>", views.StudentDetailView.as_view(), name="view_student"),
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
            template_name="registration/password_reset_form_.html", from_email=settings.NOREPLY_MAIL
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
            success_url="/matching_old/validate_email",
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
    path("validate_email", views.validate_email, name="validate_email"),
    path("profile_redirect", views.ProfileDashboardRedirect.as_view(), name="profile_redirect"),
    path("login_redirect", views.LoginRedirect.as_view(), name="login_redirect"),
    path("delete_me_ask", views.delete_me_ask, name="delete_me_ask"),
    path("delete_me", views.delete_me, name="delete_me"),
    path(
        "signup_student",
        views.ParticipantSignupView.as_view(
            template_signup="student_signup.html",
            template_thanks_for_registering="/matching_old/thanks",
            signup_form=StudentFormAndMail,
            save_form=StudentForm,
            subject_template="registration/password_reset_email_subject.txt",
            model=Student,
            mail_template="registration/password_set_email.html",
        ),
        name="student_signup",
    ),
    path(
        "signup_hospital",
        views.ParticipantSignupView.as_view(
            template_signup="hospital_signup.html",
            template_thanks_for_registering="/matching_old/thanks",
            signup_form=HospitalFormInfoSignUp,
            save_form=HospitalFormInfoCreate,
            subject_template="registration/password_reset_email_subject.txt",
            model=Hospital,
            mail_template="registration/password_set_email_hospital.html",
        ),
        name="hospital_signup",
    ),
    path("profile_student", views.StudentEditProfileView.as_view(), name="edit_student_profile"),
    path("profile_hospital", views.HospitalEditProfileView.as_view(), name="edit_hospital_profile"),
    path("approve_hospitals", views.ApproveHospitalsView.as_view(), name="approve_hospitals"),
    path(
        "change_hospital_approval/<str:uuid>/",
        views.ChangeHospitalApprovalRedirect.as_view(),
        name="change_hospital_approval",
    ),
    path(
        "delete_hospital/<str:uuid>/",
        views.DeleteHospitalRedirect.as_view(),
        name="delete_hospitall",
    ),
    path("count", views.UserCountView.as_view(), name="count"),
    path("change_activation", views.ChangeActivationAskView.as_view(), name="activate_student_ask"),
    path(
        "change_activation_confirm",
        views.ChangeActivationRedirect.as_view(),
        name="activate_student",
    ),
    path("view_newsletter/<uuid>", views.NewsletterDetailView.as_view(), name="view_newsletter"),
    path("new_newsletter", views.NewNewsletterRedirect.as_view(), name="new_newsletter"),
    path("list_newsletter", views.NewsletterListView.as_view(), name="list_newsletter"),
    path(
        "did_see_newsletter/<uuid>/<token>",
        views.ApproveNewsletterTextRedirect.as_view(),
        name="did_see_newsletter",
    ),
    path("stats", views.DBStatsView.as_view(), name="statistics"),
    path("profile_staff", views.StaffProfileView.as_view(), name="staff_profile"),
    path("i18n/", include("django.col.urls.i18n")),
]
