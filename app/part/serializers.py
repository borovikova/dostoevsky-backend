import re

from rest_framework import serializers

from .models import Part


class PartSerializer(serializers.ModelSerializer):
    clause = serializers.SerializerMethodField()

    def get_clause(self, obj):
        if re.search(r'[Вв]оинск', obj.part):
            return "Воинские преступления"
        return re.search(r'(\d{3}(\.\d{1}|))', obj.part).group()

    class Meta:
        model = Part
        fields = '__all__'
