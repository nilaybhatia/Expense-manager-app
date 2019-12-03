from django import forms
from django.contrib.auth.models import User
from .models import *

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        exclude = ['user']

class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        exclude = ['user']

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        exclude = ['user']




