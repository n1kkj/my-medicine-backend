from django.contrib import admin

from app.models import Measurement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'start_date',
        'end_date',
        'is_lifelong',
        'course',
        'user',
        'time',
        'select_time',
        'measurement_type',
        'schedule_type',
        'interval_value',
        'interval_unit',
        'selected_days_mask',
        'cycle_duration',
        'cycle_break',
        'cycle_break_unit',
    )
