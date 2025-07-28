from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class PulseData(models.Model):
    date = models.DateTimeField()
    value = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    systolic = models.IntegerField(null=True, blank=True)
    diastolic = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'pulse_data'
        verbose_name = _('Данные пульса')
        verbose_name_plural = _('Данные пульса')
