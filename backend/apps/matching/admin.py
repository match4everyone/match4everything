from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ["email"]


admin.site.register(User, UserAdmin)


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


def profile_visible_for_B(u):
    return u.is_B


def profile_visible_for_other_A(u):
    return u.is_A


def profile_visible_for_A(u):
    return u.is_A


def profile_visible_for_other_B(u):
    return u.is_B


def profile_own(uuid_accessed, uuid_own):
    return uuid_accessed == uuid_own


def required_at_least_one(restrictions_A, restrictions_B, function=None):
    def actual_decorator(function):
        def test(request, p_type, uuid, *args, **kwargs):
            u = request.user
            passes_test = False
            if p_type == "A":
                for restriction in restrictions_A:
                    passes_test += restriction(u)
            elif p_type == "B":
                for restriction in restrictions_B:
                    passes_test += restriction(u)
            passes_test += profile_own(uuid_accessed=uuid, uuid_own=u.participant().info.uuid)
            if passes_test > 0:
                return function(request, p_type, uuid, *args, **kwargs)
            raise Http404

        return test

    if function:
        return actual_decorator(function)
    return actual_decorator
