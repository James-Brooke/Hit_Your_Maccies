from django.forms import ModelForm
from .models import Food

class CalcuFilter(ModelForm):

    class Meta:
        model = Food
        fields = ['pro']
        labels = {
            'pro': ('How many grams of protein do you need?'),
        }
