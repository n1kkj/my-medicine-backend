from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.course import Course
from app.models.medicine import Medicine
from app.models.user import User


class Reminder(models.Model):
    SCHEDULE_TYPES = [
        ('interval', _('По интервалу')),
        ('weekly', _('Еженедельно')),
        ('cyclic', _('Циклически')),
        ('single', _('Однократно')),
    ]

    INTERVAL_UNITS = [
        ('days', _('Дни')),
        ('weeks', _('Недели')),
        ('months', _('Месяцы')),
    ]

    TYPE_CHOICES = [
        ('tablet', _('Лекарство')),
        ('action', _('Действие')),
        ('measurement', _('Измерение')),
    ]

    name = models.CharField(_('Название напоминания'), max_length=255)
    time = models.TimeField(_('Время срабатывания'))
    dosage = models.CharField(_('Дозировка'), max_length=100, null=True, blank=True)
    unit = models.CharField(_('Единица измерения'), max_length=50, null=True, blank=True)
    select_time = models.CharField(_('Выбранное время'), max_length=50, null=True, blank=True)
    start_date = models.DateField(_('Дата начала'))
    end_date = models.DateField(_('Дата окончания'), null=True, blank=True)
    is_lifelong = models.BooleanField(_('Бессрочное'), default=False)
    schedule_type = models.CharField(_('Тип расписания'), max_length=20, choices=SCHEDULE_TYPES)
    interval_value = models.IntegerField(_('Значение интервала'), null=True, blank=True)
    interval_unit = models.CharField(
        _('Единица интервала'), max_length=10, choices=INTERVAL_UNITS, null=True, blank=True
    )
    selected_days_mask = models.IntegerField(_('Выбранные дни (маска)'), default=0)
    cycle_duration = models.IntegerField(_('Длительность цикла'), null=True, blank=True)
    cycle_break = models.IntegerField(_('Перерыв между циклами'), null=True, blank=True)
    cycle_break_unit = models.CharField(_('Единица перерыва'), max_length=10, null=True, blank=True)
    reminder_type = models.CharField(_('Тип напоминания'), max_length=20, choices=TYPE_CHOICES, default='tablet')
    is_completed = models.BooleanField(_('Выполнено'), null=True, blank=True)
    course = models.ForeignKey(
        Course, verbose_name=_('Связанный курс'), on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    medicine = models.ForeignKey(
        Medicine, verbose_name=_('Связанное лекарство'), on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        db_table = 'reminders_table'
        verbose_name = _('Напоминание')
        verbose_name_plural = _('Напоминания')
