from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class Course(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'courses_table'
        verbose_name = _('Курс лечения')
        verbose_name_plural = _('Курсы лечения')
