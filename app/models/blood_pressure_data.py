from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class BloodPressureData(models.Model):
    date = models.DateTimeField(_('Дата и время измерения'))
    systolic = models.IntegerField(_('Систолическое давление'), help_text=_('Верхнее значение артериального давления'))
    diastolic = models.IntegerField(_('Диастолическое давление'), help_text=_('Нижнее значение артериального давления'))
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    pulse = models.IntegerField(_('Пульс'), null=True, blank=True)
    comment = models.TextField(_('Комментарий'), null=True, blank=True)

    class Meta:
        db_table = 'blood_pressure_data'
        verbose_name = _('Данные кровеносного давления')
        verbose_name_plural = _('Данные кровеносного давления')
