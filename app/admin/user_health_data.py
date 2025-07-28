from django.contrib import admin

from app.models import UserHealthData


@admin.register(UserHealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'steps', 'heart_rate', 'timestamp')
