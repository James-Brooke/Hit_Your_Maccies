from django import forms
from django.forms import ModelForm, Select
from .models import Food


CATEGORIES = (
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

class HowMuchProtein(ModelForm):

    category = forms.ChoiceField(choices=CATEGORIES, required=False)

    class Meta:
        model = Food
        fields = ['pro', 'category']    
        labels = {
            'pro': "How many grams of protein do you need?  ",
        }

class AnalyticsCategoryDropDown(ModelForm):

    category = forms.ChoiceField(choices=CATEGORIES, required=False)

    class Meta:
        model = Food
        fields = ['category']
        labels = {'category': 'Category'}

class AnalyticsMacroDropDown(forms.Form):

    macro = forms.CharField(label='Macro', widget=forms.Select(choices=MACROS))