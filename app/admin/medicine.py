from django.contrib import admin

from app.models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_form', 'quantity_in_package', 'image_path', 'package_count', 'unit', 'user')
