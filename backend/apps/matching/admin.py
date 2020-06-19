from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from .models import User

admin.site.register(User)


def participant_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Check for participants.

    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_participant, login_url=login_url, redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def participant_check(user):
    return user.is_participant
