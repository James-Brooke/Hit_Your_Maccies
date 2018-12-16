from django.forms import ModelForm
from .models import Food

class CalcuFilter(ModelForm):

    class Meta:
        model = Food
        fields = ['cal']
