from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class Medicine(models.Model):
    name = models.CharField(_('Название лекарства'), max_length=255)
    release_form = models.CharField(_('Форма выпуска'), max_length=100, null=True, blank=True)
    quantity_in_package = models.CharField(_('Количество в упаковке'), max_length=100, null=True, blank=True)
    image_path = models.CharField(_('Путь к изображению'), max_length=255, null=True, blank=True)
    package_count = models.IntegerField(_('Количество упаковок'), default=0)
    unit = models.CharField(_('Единица измерения'), max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)

    class Meta:
        db_table = 'medicines_table'
        verbose_name = _('Лекарство')
        verbose_name_plural = _('Лекарства')
