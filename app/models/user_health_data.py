from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class UserHealthData(models.Model):
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    steps = models.CharField(_('Количество шагов'), max_length=255, null=True, blank=True)
    heart_rate = models.CharField(_('Пульс'), max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(_('Дата и время'), auto_now_add=True)

    class Meta:
        db_table = 'user_health_data'
        verbose_name = _('Данные здоровья')
        verbose_name_plural = _('Данные здоровья')
