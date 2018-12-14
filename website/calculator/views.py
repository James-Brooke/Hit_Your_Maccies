from django.shortcuts import render
from django.http import HttpResponse
from .models import Food

def index(request):
    foods = Food.objects.order_by('cal')[:5]
    output = ', '.join([food.item for food in foods])
    return HttpResponse(output)

