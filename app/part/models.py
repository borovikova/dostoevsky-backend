import re

from django.db import models


class Part(models.Model):
    part = models.CharField(
        max_length=255, verbose_name='номер и часть статьи')
    name = models.CharField(
        max_length=1500, verbose_name='название части статьи')
    year = models.PositiveSmallIntegerField(verbose_name="год")
    category = models.CharField(max_length=255, null=True, verbose_name='категория статьи')
    parameters = models.JSONField(verbose_name='параметры статьи')

    def __str__(self):
        return f"{self.part} {self.name}"

    class Meta(object):
        verbose_name = "часть"
        verbose_name_plural = "части"
