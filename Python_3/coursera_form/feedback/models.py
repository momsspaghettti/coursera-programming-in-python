from django.db import models
from django.conf import settings


class Feedback(models.Model):
    """Отзыв о чем угодно"""

    text = models.CharField(verbose_name='Отзыв', max_length=5000)
    grade = models.IntegerField(verbose_name='Оценка')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(verbose_name='Объект', max_length=100)