from django.db import models
from django.utils.translation import gettext_lazy as _


class Medicine(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_path = models.CharField(_('Путь к изображению'), max_length=255, blank=True, null=True)
    name = models.TextField(_('Название лекарства'), blank=True, null=True)
    manufacturer = models.TextField(_('Производитель'), blank=True, null=True)
    origin_country = models.CharField(_('Страна происхождения'), max_length=255, blank=True, null=True)
    release_form = models.CharField(_('Форма выпуска'), max_length=255, blank=True, null=True)
    active_ingredients = models.TextField(_('Активные ингредиенты'), blank=True, null=True)
    vacation_procedure = models.TextField(_('Порядок отпуска'), blank=True, null=True)
    quantity_in_package = models.TextField(_('Количество в упаковке'), blank=True, null=True)
    barcodes = models.BigIntegerField(_('Штрих-коды'), blank=True, null=True)
    composition = models.TextField(_('Состав'), blank=True, null=True)
    description = models.TextField(_('Описание'), blank=True, null=True)
    pharmacological_effect = models.TextField(_('Фармакологическое действие'), blank=True, null=True)
    pharmacokinetics = models.TextField(_('Фармакокинетика'), blank=True, null=True)
    indications = models.TextField(_('Показания'), blank=True, null=True)
    contraindications = models.TextField(_('Противопоказания'), blank=True, null=True)
    safety_precautions = models.TextField(_('Меры предосторожности'), blank=True, null=True)
    pregnancy_usage = models.TextField(_('Применение при беременности'), blank=True, null=True)
    method_application_dosage = models.TextField(_('Способ применения и дозы'), blank=True, null=True)
    side_effects = models.TextField(_('Побочные эффекты'), blank=True, null=True)
    overdose = models.TextField(_('Передозировка'), blank=True, null=True)
    drugs_interaction = models.TextField(_('Взаимодействие с другими препаратами'), blank=True, null=True)
    special_instructions = models.TextField(_('Особые указания'), blank=True, null=True)
    storage_conditions = models.TextField(_('Условия хранения'), blank=True, null=True)

    class Meta:
        db_table = 'medicines_table'
        verbose_name = _('Лекарство')
        verbose_name_plural = _('Лекарства')
