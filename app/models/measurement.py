from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.course import Course
from app.models.reminder import Reminder
from app.models.user import User


class Measurement(models.Model):
    name = models.CharField(_('Название измерения'), max_length=255)
    start_date = models.DateField(_('Дата начала'))
    end_date = models.DateField(_('Дата окончания'), null=True, blank=True)
    is_lifelong = models.BooleanField(_('Постоянное измерение'), default=False)
    course = models.ForeignKey(
        Course, verbose_name=_('Связанный курс'), on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    time = models.TimeField(_('Время измерения'), null=True, blank=True)
    select_time = models.CharField(_('Выбранное время'), max_length=50, null=True, blank=True)
    measurement_type = models.CharField(_('Тип измерения'), max_length=20, default='measurement')
    schedule_type = models.CharField(
        _('Тип расписания'), max_length=20, choices=Reminder.SCHEDULE_TYPES, null=True, blank=True
    )
    interval_value = models.IntegerField(_('Значение интервала'), null=True, blank=True)
    interval_unit = models.CharField(
        _('Единица интервала'), max_length=10, choices=Reminder.INTERVAL_UNITS, null=True, blank=True
    )
    selected_days_mask = models.IntegerField(_('Маска выбранных дней'), default=0)
    cycle_duration = models.IntegerField(_('Длительность цикла'), null=True, blank=True)
    cycle_break = models.IntegerField(_('Длительность перерыва'), null=True, blank=True)
    cycle_break_unit = models.CharField(_('Единица перерыва'), max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'measurements_table'
        verbose_name = _('Регулярное измерение')
        verbose_name_plural = _('Регулярные измерения')
