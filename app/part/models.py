import re

from django.db import models
from django.db.models.functions import Cast
from django.db.models.fields.json import KeyTextTransform


class AggregatedDataQuerySet(models.QuerySet):
    def filter_and_aggregate(self, year=None, part=None, category=None, parameters=None, groupby=None):
        filters = {}
        if year:
            filters['year__in'] = year
        if part:
            filters['part__in'] = part
        if category:
            filters['category__in'] = category
        qs = self.filter(**filters)

        if parameters:
            annotations = dict(
                zip(
                    [f'{p}_' for p in parameters],
                    map(lambda x: Cast(KeyTextTransform(x, "parameters"), models.IntegerField()), parameters)
                )
            )
            qs = qs.annotate(**annotations)
            annotations = dict(
                zip(
                    parameters,
                    [models.Sum(f'{p}_') for p in parameters]
                )
            )
            if not groupby:
                return qs.aggregate(**annotations)
            return qs.values(*groupby).order_by().annotate(**annotations)


class Part(models.Model):
    part = models.CharField(
        max_length=255, verbose_name='номер и часть статьи')
    name = models.CharField(
        max_length=1500, verbose_name='название части статьи')
    year = models.PositiveSmallIntegerField(verbose_name="год")
    category = models.CharField(max_length=255, null=True, verbose_name='категория статьи')
    parameters = models.JSONField(verbose_name='параметры статьи')

    objects = AggregatedDataQuerySet.as_manager()

    def __str__(self):
        return f"{self.part} {self.name}"

    class Meta(object):
        verbose_name = "часть"
        verbose_name_plural = "части"
