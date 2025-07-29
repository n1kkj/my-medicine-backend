from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    surname = models.CharField(_('фамилия'), max_length=50, null=True, blank=True)
    phone = models.CharField(_('Номер телефона'), max_length=20, unique=True, null=True, blank=True)
    subscribe = models.BooleanField(_('Подписка'), default=False)
    is_logged_in = models.BooleanField(_('Залогинен'), default=False)

    class Meta:
        db_table = 'users'
        verbose_name = _('Юзер')
        verbose_name_plural = _('Юзеры')

    def __str__(self):
        return f'{self.username}'
