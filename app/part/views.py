import re
import pandas as pd

from rest_framework import generics, authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework import viewsets, mixins, response, views

from .models import Part
from part import serializers

# @swagger_auto_schema(method='get', auto_schema=None)
class PartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Не принимает никаких параметров, возвращает все имеющиеся в базе данные одним ответом.
    В Headers запроса должен быть токен `Authorization: Token <token>`"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Part.objects.all()
    serializer_class = serializers.PartSerializer


class FiltersViewSet(views.APIView):
    """Не принимает никаких параметров, возвращает все доступные метрики, годы, статьи, части  и категории.
    В Headers запроса должен быть токен `Authorization: Token <token>`"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_clause(self, part):
        if re.search(r'[Вв]оинск', part):
            return "Воинские преступления"
        return re.search(r'(\d{3}(\.\d{1}|))', part).group()
    
    def get(self, request, *args, **kwargs): 
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

