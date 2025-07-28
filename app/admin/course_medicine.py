from django.contrib import admin

from app.models import CourseMedicine


@admin.register(CourseMedicine)
class CourseMedicineAdmin(admin.ModelAdmin):
    list_display = ('course', 'medicine', 'dosage', 'unit', 'user')
