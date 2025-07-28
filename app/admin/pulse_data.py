from django.contrib import admin

from app.models import PulseData


@admin.register(PulseData)
class PulseDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'value', 'user', 'systolic', 'diastolic', 'comment')
