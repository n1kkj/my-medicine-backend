from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class Medicine(models.Model):
    name = models.CharField(max_length=255)
    release_form = models.CharField(max_length=100, null=True, blank=True)
    quantity_in_package = models.CharField(max_length=100, null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    package_count = models.IntegerField(default=0)
    unit = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'medicines_table'
        verbose_name = _('Лекарство')
        verbose_name_plural = _('Лекарства')
