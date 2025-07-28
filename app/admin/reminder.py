from django.contrib import admin

from app.models import Reminder, ReminderStatus


class ReminderStatusInline(admin.TabularInline):
    model = ReminderStatus
    extra = 0
    readonly_fields = ('date', 'is_completed')


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'time',
        'dosage',
        'unit',
        'select_time',
        'start_date',
        'end_date',
        'is_lifelong',
        'schedule_type',
        'interval_value',
        'interval_unit',
        'selected_days_mask',
        'cycle_duration',
        'cycle_break',
        'cycle_break_unit',
        'reminder_type',
        'is_completed',
        'course',
        'user',
        'medicine',
    )
    inlines = [ReminderStatusInline]

    def is_active(self, obj):
        return not obj.is_completed

    is_active.boolean = True
