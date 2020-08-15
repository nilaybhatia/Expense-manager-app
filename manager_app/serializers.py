from rest_framework import serializers
from .models import Income, Savings, Expenditure

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        exclude = ['user']

class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savings
        exclude = ['user']

class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenditure
        exclude = ['user']