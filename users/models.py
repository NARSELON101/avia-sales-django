import uuid

from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    usr_uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    is_activated = models.BooleanField(default=False)
