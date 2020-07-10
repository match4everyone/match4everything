from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

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


def matching_participant_required(function=None):
    """
    Check that participant matches url.

    Decorator for views that checks that the user is logged in,
    and that the user matches to the /<p_type:p_type> url
    """

    def actual_decorator(function):
        def new_func(request, p_type, *args, **kwargs):
            if (request.user.is_A and p_type == "A") or (request.user.is_B and p_type == "B"):
                return function(request, p_type, *args, **kwargs)
            raise Http404

        return new_func

    if function:
        return actual_decorator(function)
    return actual_decorator


def logged_in_not_permitted(function=None, login_url="/"):
    """
    Decorator for views that checks that the user is not logged in.

    Redirecting to the home page if necessary.
    """
    actual_decorator = user_passes_test(lambda u: not u.is_authenticated, login_url="/",)
    if function:
        return actual_decorator(function)
    return actual_decorator
