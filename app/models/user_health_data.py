from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class UserHealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.CharField(max_length=255, null=True, blank=True)
    heart_rate = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_health_data'
        verbose_name = _('Данные здоровья')
        verbose_name_plural = _('Данные здоровья')
