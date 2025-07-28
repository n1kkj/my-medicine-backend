from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.course import Course
from app.models.medicine import Medicine
from app.models.user import User


class CourseMedicine(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'course_medicines'
        verbose_name = _('Лекарство в курсе')
        verbose_name_plural = _('Лекарства в курсе')
