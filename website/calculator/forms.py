from django import forms
from django.forms import ModelForm, Select
from .models import Food


CATEGORIES = (
    ('ALL', 'All'),
    ('CHICKEN', 'Chicken'),
    ('BURGER', 'Beef'),
    ('BEVERAGE', 'Drinks'),
    ('BREAKFAST', 'Breakfast'),
    ('DESSERT', 'Dessert'),
    ('HAPPYMEAL', 'Happy Meals')
    )

class HowMuchProtein(ModelForm):

    category = forms.ChoiceField(choices=CATEGORIES, required=False)

    class Meta:
        model = Food
        fields = ['pro', 'category']    
        labels = {
            'pro': "How many grams of protein do you need?  ",
        }

class AnalyticsDropDown(ModelForm):

    category = forms.ChoiceField(choices=CATEGORIES, required=False)

    class Meta:
        model = Food
        fields = ['category']
        labels = {'category': 'Category'}