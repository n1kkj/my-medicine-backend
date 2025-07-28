from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class StepsData(models.Model):
    date = models.DateTimeField()
    count = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'steps_data'
        verbose_name = _('Данные шагов')
        verbose_name_plural = _('Данные шагов')
