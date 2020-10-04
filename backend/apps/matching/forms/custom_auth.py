from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _


class CustomUserNameField(UsernameField):
    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autofocus": True,
            "autocomplete": "username email",
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = CustomUserNameField(label=_("E-Mail"), widget=forms.TextInput())
