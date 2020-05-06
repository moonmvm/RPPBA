# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Dmitry Mishuto <dmitry.mishuto@celadon.ae>

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from rppba.settings import AUTH_USER_MODEL


class User(AbstractUser):

    amount_of_waybills = models.PositiveIntegerField(default=0)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
