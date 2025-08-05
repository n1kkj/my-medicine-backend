from django.db import models
from django.utils.translation import gettext_lazy as _


class Medicine(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_path = models.TextField(_('Путь к изображению'), max_length=255, blank=True, null=True, db_column='ImagePath')
    name = models.TextField(_('Название лекарства'), blank=True, null=True, db_column='Name')
    manufacturer = models.TextField(_('Производитель'), blank=True, null=True, db_column='Manufacturer')
    origin_country = models.TextField(_('Страна происхождения'), max_length=255, blank=True, null=True, db_column='OriginCountry')
    release_form = models.TextField(_('Форма выпуска'), max_length=255, blank=True, null=True, db_column='ReleaseForm')
    active_ingredients = models.TextField(_('Активные ингредиенты'), blank=True, null=True, db_column='ActiveIngredients')
    vacation_procedure = models.TextField(_('Порядок отпуска'), blank=True, null=True, db_column='VacationProcedure')
    quantity_in_package = models.TextField(_('Количество в упаковке'), blank=True, null=True, db_column='QuantityInPackage')
    barcodes = models.TextField(_('Штрих-коды'), blank=True, null=True, db_column='Barcodes')
    composition = models.TextField(_('Состав'), blank=True, null=True, db_column='Composition')
    description = models.TextField(_('Описание'), blank=True, null=True, db_column='Description')
    pharmacological_effect = models.TextField(_('Фармакологическое действие'), blank=True, null=True, db_column='PharmacologicalEffect')
    pharmacokinetics = models.TextField(_('Фармакокинетика'), blank=True, null=True, db_column='Pharmacokinetics')
    indications = models.TextField(_('Показания'), blank=True, null=True, db_column='Indications')
    contraindications = models.TextField(_('Противопоказания'), blank=True, null=True, db_column='Contraindications')
    safety_precautions = models.TextField(_('Меры предосторожности'), blank=True, null=True, db_column='SafetyPrecautions')
    pregnancy_usage = models.TextField(_('Применение при беременности'), blank=True, null=True, db_column='PregnancyUsage')
    method_application_dosage = models.TextField(_('Способ применения и дозы'), blank=True, null=True, db_column='MethodApplicationDosage')
    side_effects = models.TextField(_('Побочные эффекты'), blank=True, null=True, db_column='SideEffects')
    overdose = models.TextField(_('Передозировка'), blank=True, null=True, db_column='Overdose')
    drugs_interaction = models.TextField(_('Взаимодействие с другими препаратами'), blank=True, null=True, db_column='DrugsInteraction')
    special_instructions = models.TextField(_('Особые указания'), blank=True, null=True, db_column='SpecialInstructions')
    storage_conditions = models.TextField(_('Условия хранения'), blank=True, null=True, db_column='StorageConditions')

    class Meta:
        db_table = 'Medicines'
        verbose_name = _('Лекарство')
        verbose_name_plural = _('Лекарства')
