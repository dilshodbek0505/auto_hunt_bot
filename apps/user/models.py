from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.common.models import BaseModel



class User(AbstractUser, BaseModel):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"