from django.contrib import admin

from app.admin.user_health_data import HealthDataAdmin
from app.models import BloodPressureData


@admin.register(BloodPressureData)
class BloodPressureDataAdmin(HealthDataAdmin):
    list_display = ('date', 'systolic', 'diastolic', 'user', 'pulse', 'comment')
