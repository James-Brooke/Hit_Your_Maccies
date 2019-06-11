from django import forms
from django.forms import ModelForm, Select
from .models import Food


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

    protein_placeholder = "How many grams of protein do you need?"
    category_placeholder = "Category"

    protein = forms.IntegerField(label='',
                                 required=False, 
                                 widget=forms.NumberInput(
                                    attrs={'placeholder': protein_placeholder}))
    category = forms.ChoiceField(label='',
                                 choices=CATEGORIES, 
                                 required=False,
                                 widget=forms.Select(
                                    attrs={'placeholder': category_placeholder}))


class AnalyticsCategoryDropDown(ModelForm):

    category = forms.ChoiceField(choices=CATEGORIES[1:], required=False)

    class Meta:
        model = Food
        fields = ['category']
        labels = {'category': 'Category'}

class AnalyticsMacroDropDown(forms.Form):

    macro = forms.CharField(label='Macro', 
        widget=forms.Select(choices=MACROS), required=False)
