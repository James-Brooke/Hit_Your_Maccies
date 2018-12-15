from django.shortcuts import render
from django.http import HttpResponse
from .models import Food

def index(request):
    foods = Food.objects.order_by('-cal')[:5]
    context = {'foods': foods,}
    return render(request, 'calculator/index.html', context)

