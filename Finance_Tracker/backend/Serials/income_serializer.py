from rest_framework import serializers
from ..Models.income_information import IncomeModel

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeModel
        fields = '__all__'
        read_only_fields = ['user']