from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class BloodPressureData(models.Model):
    date = models.DateTimeField()
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pulse = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'blood_pressure_data'
        verbose_name = _('Данные кровеносного давления')
        verbose_name_plural = _('Данные кровеносного давления')
