from django.contrib import admin

from app.models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'manufacturer',
        'release_form',
        'active_ingredients',
        'origin_country',
        'image_path'
    )
    list_filter = (
        'manufacturer',
        'origin_country',
        'release_form',
    )
    search_fields = (
        'name',
        'manufacturer',
        'active_ingredients',
        'composition',
    )
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name',
                'manufacturer',
                'image_path',
                'release_form',
                'quantity_in_package',
                'origin_country',
                'barcodes'
            )
        }),
        ('Состав и свойства', {
            'fields': (
                'active_ingredients',
                'composition',
                'pharmacological_effect',
                'pharmacokinetics',
            ),
            'classes': ('collapse',)
        }),
        ('Применение', {
            'fields': (
                'indications',
                'contraindications',
                'method_application_dosage',
                'pregnancy_usage',
            ),
            'classes': ('collapse',)
        }),
        ('Дополнительная информация', {
            'fields': (
                'side_effects',
                'overdose',
                'drugs_interaction',
                'storage_conditions',
            ),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('id',)
