from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Test Pages
    path("dummy", views.send_dummy_mail, name="dummy"),
    path("editor", views.MailEditor.as_view(), name="editor"),
    # Email-Base template view
    path("template_view", TemplateView.as_view(template_name="base_mail.html"), name="template-view"),

    # Real pages
    path("contact_student", views.ContactMassEditor.as_view(), name="contact_student"),
    # Email-Base template view
    path("template_preview/<uuid:template_name>", views.EmailTemplatePreview.as_view(), name="email_template_preview"),
    path("send_mails", views.SendMailView.as_view(), name="send_mails"),
]
