from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.course import Course
from app.models.medicine import Medicine
from app.models.user import User


class Reminder(models.Model):
    SCHEDULE_TYPES = [
        ('interval', 'По интервалу'),
        ('weekly', 'Еженедельно'),
        ('cyclic', 'Циклически'),
        ('single', 'Однократно'),
    ]

    INTERVAL_UNITS = [
        ('days', 'Дни'),
        ('weeks', 'Недели'),
        ('months', 'Месяцы'),
    ]

    TYPE_CHOICES = [
        ('tablet', 'Лекарство'),
        ('action', 'Действие'),
        ('measurement', 'Измерение'),
    ]

    name = models.CharField(max_length=255)
    time = models.TimeField()
    dosage = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    select_time = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_lifelong = models.BooleanField(default=False)
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPES)
    interval_value = models.IntegerField(null=True, blank=True)
    interval_unit = models.CharField(max_length=10, choices=INTERVAL_UNITS, null=True, blank=True)
    selected_days_mask = models.IntegerField(default=0)
    cycle_duration = models.IntegerField(null=True, blank=True)
    cycle_break = models.IntegerField(null=True, blank=True)
    cycle_break_unit = models.CharField(max_length=10, null=True, blank=True)
    reminder_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='tablet')
    is_completed = models.BooleanField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'reminders_table'
        verbose_name = _('Напоминание')
        verbose_name_plural = _('Напоминания')
