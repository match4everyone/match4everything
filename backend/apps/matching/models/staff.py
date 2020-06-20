from django.db import models

from .user import User


class Staff(models.Model):
    """An admin class for organizing the different access classes for maintainers of the platform."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    @staticmethod
    def new(mail, pwd):
        user = User.new(email=mail, pwd=pwd, is_staff=True)
        staff = Staff.objects.create(user=user)
        return staff
