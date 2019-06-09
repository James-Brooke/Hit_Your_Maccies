from django import forms
from django.forms import ModelForm, Select
from .models import Food

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


CATEGORIES = (
    ('ALL', 'Any'),
    ('CHICKEN', 'Chicken'),
    ('BURGER', 'Beef'),
    ('BEVERAGE', 'Drinks'),
    ('BREAKFAST', 'Breakfast'),
    ('DESSERT', 'Dessert'),
    ('HAPPYMEAL', 'Happy Meals')
    )

MACROS = (
    ('cal', 'Calories'),
    ('pro', 'Protein') 
)

class HowMuchProtein(forms.Form):

    protein = forms.IntegerField(initial=25, label= "How many grams of protein do you need? ")
    category = forms.ChoiceField(choices=CATEGORIES, required=False)

class AnalyticsCategoryDropDown(ModelForm):

    category = forms.ChoiceField(choices=CATEGORIES, required=False)

    class Meta:
        model = Food
        fields = ['category']
        labels = {'category': 'Category'}

class AnalyticsMacroDropDown(forms.Form):

    macro = forms.CharField(label='Macro', widget=forms.Select(choices=MACROS))

