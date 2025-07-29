from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.reminder import Reminder
from app.models.user import User


class ReminderStatus(models.Model):
    reminder = models.ForeignKey(_('Напоминание'), Reminder, on_delete=models.CASCADE)
    date = models.DateField(_('Дата'))
    is_completed = models.BooleanField(_('Закончен'))
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)

    class Meta:
        db_table = 'reminder_statuses'
        verbose_name = _('Статус напоминания')
        verbose_name_plural = _('Статусы напоминаний')
