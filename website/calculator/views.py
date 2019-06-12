import math
import json
import copy

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Food
from .forms import HowMuchProtein, AnalyticsCategoryDropDown, AnalyticsMacroDropDown


def calculate_quantity(food, protein_required):
    """Calculates how many of each item is required to hit requirements.
    
    :food: a Food item
    :requirements: grams of protein required
    :returns: int: the number of food items required to hit protein_required
    """
    protein = float(food.pro)
    if protein < 0.01:
        return 0
    if protein > protein_required:
        quantity = 1 
    else:
        quantity = math.ceil(protein_required / protein)
    return quantity

def l2_distance(food, protein):
    return math.sqrt(protein**2 - food.total_protein**2)

def create_food_list(food_manager, category, protein_required):

    if category != 'ALL':
        foods = food_manager.filter(category=category)
    else:
        foods = food_manager.all()

    for food in foods:
        # calculate how many of this item required to hit macros
        food.quantity = calculate_quantity(food, protein_required)
        food.total_protein = food.pro * food.quantity

    # remove items with excessive macros
    food_list = [x for x in foods if x.quantity > 0 and 
                    ( (protein_required+10) >= x.total_protein)] 
    food_list = sorted(food_list, key=lambda x: x.total_protein)

    best = copy.deepcopy(food_list[0])
    best.pro *= best.quantity
    best.cal *= best.quantity
    best.fat *= best.quantity
    best.sfat *= best.quantity
    best.carb *= best.quantity
    best.sgr *= best.quantity
    best.salt *= best.quantity
    best.fbr *= best.quantity

    return food_list, best
    

def index(request):
    """Returns the home view.
    
    When the request is a GET, the view includes a form.
    When the request is a POST, the view includes a table of results.
    """
    context = { 'home_page': 'active',
                'get': True if request.method != 'POST' else False}

    if not context['get']:

        # Retrieve data from form
        form = HowMuchProtein(request.POST)
        if form.is_valid():
            protein_required = float(form.cleaned_data['protein'])
            category = form.cleaned_data['category']
        else:
            raise ValueError('InvalidForm')

        # Find list of foods that meet requirements
        food_list, best = create_food_list(Food.objects, category, protein_required)

        context['best'] = best
        context['protein'] = protein_required
        context['foods'] = food_list

    else:
        context['form'] = HowMuchProtein()

    return render(request, 'calculator/index.html', context)


def analytics(request):
    """Returns analytics view."""
    category_dropdown = AnalyticsCategoryDropDown()
    macro_dropdown = AnalyticsMacroDropDown()
    context = { 'analytics_page': 'active',
                'category_dropdown': category_dropdown, 
                'macro_dropdown': macro_dropdown}
    return render(request, 'calculator/analytics.html', context)


def contact(request):
    """Returns contact view."""
    context = { 'contact_page': 'active'}
    return render(request, 'calculator/contact.html', context)


def data(request):
    """Restful API used by analytics view.
    
    Returns JSON of all food items stored in DB."""
    data = serializers.serialize('json', Food.objects.all())
    data = json.loads(data)
    return JsonResponse(data, safe=False)