from django.db import models
from django.contrib.auth.models import AbstractUser


class UserLogin(AbstractUser):
    is_online = models.BooleanField(default = False)