from django.contrib import admin

from app.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'start_date',
        'end_date',
        'is_lifelong',
        'course',
        'user',
        'time',
        'action_type',
        'select_time',
        'quantity',
        'schedule_type',
        'interval_value',
        'interval_unit',
        'selected_days_mask',
        'cycle_duration',
        'cycle_break',
        'cycle_break_unit',
        'notification',
        'is_completed',
        'times',
    )
