from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class PulseData(models.Model):
    date = models.DateTimeField(_('Дата и время измерения'))
    value = models.IntegerField(_('Значение пульса'))
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    systolic = models.IntegerField(_('Систолическое давление'), null=True, blank=True)
    diastolic = models.IntegerField(_('Диастолическое давление'), null=True, blank=True)
    comment = models.TextField(_('Комментарий'), null=True, blank=True)

    class Meta:
        db_table = 'pulse_data'
        verbose_name = _('Данные пульса')
        verbose_name_plural = _('Данные пульса')
