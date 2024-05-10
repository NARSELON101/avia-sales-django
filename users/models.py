import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_activated = models.BooleanField(default=False)
    is_receive_news = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'auth_user'
