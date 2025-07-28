from django.contrib import admin

from app.models import StepsData


@admin.register(StepsData)
class StepsDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'count', 'user', 'comment')
