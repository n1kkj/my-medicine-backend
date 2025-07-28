from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.course import Course
from app.models.reminder import Reminder
from app.models.user import User


class Action(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_lifelong = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.TimeField(null=True, blank=True)
    action_type = models.CharField(max_length=20, default='action')
    select_time = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.CharField(max_length=100, null=True, blank=True)
    schedule_type = models.CharField(max_length=20, choices=Reminder.SCHEDULE_TYPES, null=True, blank=True)
    interval_value = models.IntegerField(null=True, blank=True)
    interval_unit = models.CharField(max_length=10, choices=Reminder.INTERVAL_UNITS, null=True, blank=True)
    selected_days_mask = models.IntegerField(default=0)
    cycle_duration = models.IntegerField(null=True, blank=True)
    cycle_break = models.IntegerField(null=True, blank=True)
    cycle_break_unit = models.CharField(max_length=10, null=True, blank=True)
    notification = models.CharField(max_length=255, null=True, blank=True)
    is_completed = models.BooleanField(null=True, blank=True)
    times = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'actions_table'
