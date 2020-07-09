from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


"""
Simple methods for deleting users.
Could possibly be class based.
"""


@login_required
def delete_me(request, p_type):
    user = request.user
    logout(request)
    user.delete()
    return render(request, "messages/deleted_user.html")


@login_required
def delete_me_ask(request, p_type):
    return render(request, "messages/deleted_user_ask.html")
