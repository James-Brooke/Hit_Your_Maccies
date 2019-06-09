import math
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Food
from .forms import HowMuchProtein, AnalyticsCategoryDropDown, AnalyticsMacroDropDown


def process_food(food, protein_required):
    protein = float(food.pro)
    if protein < 0.01:
        return 0
    if protein > protein_required:
        quantity = 1 
    else:
        quantity = math.ceil(protein_required / protein)
    return quantity


def index(request):

    if request.method == 'POST':
        get = False
        protein = float(request.POST['protein'])
        category = request.POST['category']
        foods = Food.objects.order_by('-pro')
        if category != 'ALL':
            foods = foods.filter(category=category)

        foods = list(foods) # force evaluation of queryset to allow extra attributes to be set
        for food in foods:
            food.quantity = process_food(food, protein) # calculate how many of this item to hit requirements
            food.total_protein = food.pro * food.quantity
        foods[:] = [x for x in foods if (x.quantity * x.pro <= (protein+10)) and x.quantity > 0] # remove items with excessive macros
        foods[:] = sorted(foods, key=lambda x: x.total_protein)
        best = foods[0]
        best.pro *= best.quantity
        best.cal *= best.quantity
        best.fat *= best.quantity
        best.sfat *= best.quantity
        best.carb *= best.quantity
        best.sgr *= best.quantity
        best.salt *= best.quantity
        best.fbr *= best.quantity

        form = HowMuchProtein(request.POST)

        if form.is_valid():
            pass #trigger validation
        
    else:
        form = HowMuchProtein()
        foods = Food.objects.order_by('-cal')[:1]
        get = True

    context = { 'home_page': 'active',
                'foods': foods,
                'form': form,
                'get': get}
    if not get:
        context['best'] = best
        context['protein'] = protein
    

    return render(request, 'calculator/index.html', context)


def analytics(request):
    category_dropdown = AnalyticsCategoryDropDown()
    macro_dropdown = AnalyticsMacroDropDown()
    context = { 'analytics_page': 'active',
                'category_dropdown': category_dropdown, 
                'macro_dropdown': macro_dropdown}
    return render(request, 'calculator/analytics.html', context)


def about(request):
    context = { 'about_page': 'active'}
    return render(request, 'calculator/about.html', context)


def contact(request):
    context = { 'contact_page': 'active'}
    return render(request, 'calculator/contact.html', context)

def data(request):

    data = serializers.serialize('json', Food.objects.all())
    data = json.loads(data)
    return JsonResponse(data, safe=False)