from rest_framework import generics, mixins, response, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from app.constants import FILTERS, UNCOUNTABLE
from .models import Part
from .serializers import (AggregatedDataSerializer,
                          PartSerializer,
                          TablePartSerializer)
from .utils import prepare_query_params, get_all_filters, add_filters_to_response


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

    def list(self, request, *args, **kwargs):
        return response.Response(get_all_filters())


class AggregatedDataView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, year, part, params, breakdowns):
        countable_params = [p for p in params if p not in UNCOUNTABLE]
        groupby = breakdowns.copy()
        if 'part' in breakdowns or len(part) == 1:
            groupby.append('name')

        return Part.objects.filter_and_aggregate(year, part, countable_params, groupby)

    def post(self, request, *args, **kwargs):
        year, part, params, breakdowns = [request.data.get(param) for param in FILTERS]
        if not all([year, part, params]):
            return response.Response([])
        data = self.prepare_data(year, part, params, breakdowns)
        return response.Response(data)

    def list(self, request, *args, **kwargs):
        year, part, params, breakdowns = prepare_query_params(request.query_params)
        if not all([year, part, params]):
            return response.Response([])
        data = self.prepare_data(year, part, params, breakdowns)
        return response.Response(data)

    def prepare_data(self, year, part, params, breakdowns):
        data = []
        context = {
            'year': year,
            'part': part,
            'param': params,
            'breakdowns': breakdowns
        }

        if len(breakdowns) == 1:
            data = AggregatedDataSerializer(self.get_queryset(year, part, params, breakdowns), many=True,
                                            context=context).data
            if not data:
                data = [add_filters_to_response(year, part, params, breakdowns, {})]

        elif len(breakdowns) == 0:
            if len(year) == 1 and len(part) == 1:
                data = AggregatedDataSerializer(self.get_queryset(year, part, params, breakdowns), many=True,
                                                context=context).data
                if not data:
                    data = [add_filters_to_response(year, part, params, breakdowns, {})]
            elif len(part) == 1:
                data = AggregatedDataSerializer(self.get_queryset(year, part, params, breakdowns), many=True,
                                                context=context).data
                if not data:
                    data = [add_filters_to_response(year, part, params, breakdowns, {})]
            else:
                data = AggregatedDataSerializer(self.get_queryset(
                    year, part, params, breakdowns), context=context).data or {}
                data = [add_filters_to_response(year, part, params, breakdowns, data)]


        elif len(breakdowns) == 2:
            filters = {}
            if year:
                filters['year__in'] = year
            if part:
                filters['part__in'] = part
            qs = Part.objects.filter(**filters)
            data = TablePartSerializer(qs, many=True, context=context).data

        data = sorted(data, key=lambda item: (item["year"], item["part"]))
        return data
