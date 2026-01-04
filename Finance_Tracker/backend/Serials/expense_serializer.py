from rest_framework import serializers
from ..Models.expense_information import ExpenseModel

#View information in the model all at once

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseModel
        fields = '__all__'
        read_only_fields = ['user']
