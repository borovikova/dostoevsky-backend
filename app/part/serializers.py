import re

from app.constants import FILTERS
from rest_framework import serializers

from .models import Part
from .utils import add_filters_to_response


class PartSerializer(serializers.ModelSerializer):
    clause = serializers.SerializerMethodField()

    def get_clause(self, obj):
        if re.search(r'[Вв]оинск', obj.part):
            return "Воинские преступления"
        return re.search(r'(\d{3}(\.\d{1}|))', obj.part).group()

    class Meta:
        model = Part
        fields = '__all__'


class AggregatedDataSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        ret = add_filters_to_response(*[self.context.get(param) for param in FILTERS], instance)
        return ret


class TablePartSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        params = self.context.get('param')

        ret.update({k: ret.get('parameters', {}).get(k) for k in ret.get('parameters', {}) if k in params})
        ret.pop('parameters', None)
        ret.pop('id', None)
        ret.pop('category', None)
        return ret

    class Meta:
        model = Part
        fields = '__all__'
