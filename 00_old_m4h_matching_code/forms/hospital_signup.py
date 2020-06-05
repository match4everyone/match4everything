from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from apps.matching_old.models import User

# sign up with info used


class ParticipantSignUpForm(UserCreationForm):
    # add more query fields

    class Meta(UserCreationForm.Meta):
        model = User
        fields = []  # ['email']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_participant = True
        user.save()
        return user
