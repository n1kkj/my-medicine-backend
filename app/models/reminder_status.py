from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.reminder import Reminder
from app.models.user import User


class ReminderStatus(models.Model):
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    date = models.DateField()
    is_completed = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reminder_statuses'
        verbose_name = _('Статус напоминания')
        verbose_name_plural = _('Статусы напоминаний')
