import logging

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class User(AbstractUser):

    # participant p_type
    is_participant = models.BooleanField(default=False)
    is_A = models.BooleanField(default=False)
    is_B = models.BooleanField(default=False)

    # email validation
    validated_email = models.BooleanField(default=False)
    email_validation_date = models.DateTimeField(blank=True, null=True)

    REQUIRED_FIELDS = ["email"]

    @staticmethod
    def validate_email_not_taken(value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(_("This email is already taken."))
        return value

    @staticmethod
    def new(email, pwd=None, **kwargs):
        username = email
        user = User.objects.create(username=username, email=username, **kwargs)
        if pwd is not None:
            user.set_password(pwd)
        else:
            user.set_password(get_random_string(length=32))
        user.save()
        return user

    def participant(self):
        if self.is_A:
            return self.a
        if self.is_B:
            return self.b

    class Meta(AbstractUser.Meta):
        constraints = [
            # we can only have either participant a or participant b for one user
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_has_only_one_participant",
                check=(~(models.Q(is_A=True) & models.Q(is_B=True))),
            ),
            # only either staff or participant or none
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_only_staff_or_participant_or_none",
                check=(models.Q(is_participant=False) | models.Q(is_staff=False)),
            ),
        ]
