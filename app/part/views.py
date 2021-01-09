import re
import pandas as pd

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins, views, generics, response

from .models import Part
from .serializers import PartSerializer, AggregatedDataSerializer, TablePartSerializer
from .utils import prepare_query_params, add_filters_to_response
from app.constants import UNCOUNTABLE


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


class AggregatedDataView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        year, part, category, params, breakdowns = prepare_query_params(self.request.query_params)

        countable_params = [p for p in params if p not in UNCOUNTABLE]
        groupby = breakdowns
        if 'part' in breakdowns or len(part) == 1:
            groupby.append('name')

        return Part.objects.filter_and_aggregate(year, part, category, countable_params, groupby)

    def list(self, request, *args, **kwargs):
        year, part, category, params, breakdowns = prepare_query_params(request.query_params)

        if len(breakdowns) == 1:
            data = AggregatedDataSerializer(self.get_queryset(), many=True, context={'request': request}).data
        
        if len(breakdowns) == 0:
            if len(year) == 1 and len(part) == 1:
                data = AggregatedDataSerializer(self.get_queryset(), many=True, context={'request': request}).data
            elif len(year) == 1 or len(part) == 1:
                data = AggregatedDataSerializer(self.get_queryset(), many=True, context={'request': request}).data
            else:
                data = AggregatedDataSerializer(self.get_queryset(), context={'request': request}).data

        if len(breakdowns) == 2:
            filters = {}
            if year:
                filters['year__in'] = year
            if part:
                filters['part__in'] = part
            if category:
                filters['category__in'] = category
            qs = Part.objects.filter(**filters)
            data = TablePartSerializer(qs, many=True, context={'request': request}).data

        return response.Response(data)
