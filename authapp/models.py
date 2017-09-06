from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    """
    model for extra info of the user
    """
    user = models.OneToOneField(User)
    login_type = models.BooleanField(default=True)  # True means API backend and False means FB login
    auth_token = models.CharField(max_length=64, null=True, default=None)