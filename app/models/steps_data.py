from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.user import User


class StepsData(models.Model):
    date = models.DateTimeField(_('Дата и время'))
    count = models.IntegerField(_('Количество шагов'))
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    comment = models.TextField(_('Комментарий'), null=True, blank=True)

    class Meta:
        db_table = 'steps_data'
        verbose_name = _('Данные шагов')
        verbose_name_plural = _('Данные шагов')
