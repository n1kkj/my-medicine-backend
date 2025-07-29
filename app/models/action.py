from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.course import Course
from app.models.reminder import Reminder
from app.models.user import User


class Action(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    start_date = models.DateField(_('Дата начала'))
    end_date = models.DateField(_('Дата окончания'), null=True, blank=True)
    is_lifelong = models.BooleanField(_('Пожизненное действие'), default=False)
    course = models.ForeignKey(
        Course, verbose_name=_('Связанный курс'), on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    time = models.TimeField(_('Время выполнения'), null=True, blank=True)
    action_type = models.CharField(_('Тип действия'), max_length=20, default='action')
    select_time = models.CharField(_('Выбранное время'), max_length=50, null=True, blank=True)
    quantity = models.CharField(_('Количество'), max_length=100, null=True, blank=True)
    schedule_type = models.CharField(
        _('Тип расписания'), max_length=20, choices=Reminder.SCHEDULE_TYPES, null=True, blank=True
    )
    interval_value = models.IntegerField(_('Значение интервала'), null=True, blank=True)
    interval_unit = models.CharField(
        _('Единица измерения интервала'), max_length=10, choices=Reminder.INTERVAL_UNITS, null=True, blank=True
    )
    selected_days_mask = models.IntegerField(_('Маска выбранных дней'), default=0)
    cycle_duration = models.IntegerField(_('Длительность цикла'), null=True, blank=True)
    cycle_break = models.IntegerField(_('Перерыв между циклами'), null=True, blank=True)
    cycle_break_unit = models.CharField(_('Единица измерения перерыва'), max_length=10, null=True, blank=True)
    notification = models.CharField(_('Уведомление'), max_length=255, null=True, blank=True)
    is_completed = models.BooleanField(_('Выполнено'), null=True, blank=True)
    times = models.CharField(_('Времена выполнения'), max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'actions_table'
        verbose_name = _('Привычка')
        verbose_name_plural = _('Привычки')

    def __str__(self):
        return f'{self.name} ({self.user})'
