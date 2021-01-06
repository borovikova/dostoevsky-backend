import json
import re
import pandas as pd

from rest_framework import generics, authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework import viewsets, mixins, response, views

from .models import Part
from .serializers import PartSerializer


class PartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Не принимает никаких параметров, возвращает все имеющиеся в базе данные одним ответом.
    В Headers запроса должен быть токен `Authorization: Token <token>`"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class FiltersViewSet(viewsets.GenericViewSet):
    """Не принимает никаких параметров, возвращает все доступные метрики, годы, статьи, части  и категории.
    В Headers запроса должен быть токен `Authorization: Token <token>`"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_clause(self, part):
        if re.search(r'[Вв]оинск', part):
            return "Воинские преступления"
        return re.search(r'(\d{3}(\.\d{1}|))', part).group()

    def list(self, request, *args, **kwargs):
        # TODO: переписать на работу с базой
        df = pd.DataFrame(Part.objects.order_by('part').values())

        parts = df.drop_duplicates(subset=['part'])['part'].values.tolist()
        clauses = sorted(list(set([self.get_clause(part) for part in parts])))
        years = df.drop_duplicates(subset=['year'])['year'].values.tolist()
        categories = df.drop_duplicates(subset=['category']).dropna()['category'].values.tolist()

        df.loc[:, 'params'] = df.apply(lambda row: list(row.parameters.keys()), axis=1)
        df = df.explode('params')
        params = sorted(df.drop_duplicates(subset=['params'])['params'].values.tolist())

        data = {
            "clause": clauses,
            "part": parts,
            "year": years,
            "category": categories,
            "parameters": params
        }
        return response.Response(data)


class AggregatedDataViewSet(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Part.objects.all()
    uncountable = ["addTotalPersons", "addTotalOffences", "addAcquittalPersons", "addAcquittalOffences",
                   "addDismissalPersons", "addDismissalOffences", "addDismissalOtherPersons",
                   "addDismissalOtherOffences", "addUnfitToPleadPersons", "addUnfitToPleadOffences"]

    def list(self, request, *args, **kwargs):

        year = self.request.query_params.get('year')
        if year:
            year = year.split(',')

        part = self.request.query_params.get('part')
        if part:
            part = part.split(',')

        category = self.request.query_params.get('category')
        if category:
            category = category.split(',')

        params = self.request.query_params.get('param')
        params = params.split(',') if params else []
        countable_params = [p for p in params if p not in self.uncountable]

        breakdowns = self.request.query_params.get('breakdowns')
        breakdowns = breakdowns.split(',') if breakdowns else []
        grouby_params = {
            'year': 'part',
            'part': 'year'
        }
        groupby = [grouby_params[_] for _ in breakdowns if _ in grouby_params.keys()]

        qs = self.queryset.filter_and_aggregate(year, part, category, countable_params, groupby)

        if len(breakdowns)==2:
            qs = qs.values('part', 'name', 'year', 'parameters')

        data = list(qs) if breakdowns else [qs]

        def add_unaggregated_params(row):
            if part and 'year' not in breakdowns:
                row['part'] = ', '.join(sorted(part))
            if year and 'part' not in breakdowns:
                if len(year) > 1:
                    years = [int(_) for _ in year]
                    row['year'] = '-'.join([str(min(years)), str(max(years))])
                else:
                    row['year'] = year[0]
            if len(breakdowns) != 2:
                row.update({param: None for param in params if param in self.uncountable})
                row.update({'name': None})
            else:
                row.update({param:row.get('parameters', {}).get(param) for param in params})
                row.pop('parameters')
            return row

        data = list(map(add_unaggregated_params, data))

        return response.Response(data)
