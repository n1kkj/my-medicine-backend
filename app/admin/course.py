from django.contrib import admin

from app.models import Course, CourseMedicine


class CourseMedicineInline(admin.TabularInline):
    model = CourseMedicine
    extra = 1
    raw_id_fields = ('medicine',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    inlines = [CourseMedicineInline]
    search_fields = ('name', 'user__username')
