from rest_framework import serializers
from ..Models.debt_information import DebtModel, InDebtModel

class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtModel
        fields = '__all__'
        read_only_fields = ['user']
        

class InDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = InDebtModel
        fields = '__all__'
