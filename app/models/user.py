from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    subscribe = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
        verbose_name = _('Юзер')
        verbose_name_plural = _('Юзеры')

    def __str__(self):
        return f'{self.username}'
