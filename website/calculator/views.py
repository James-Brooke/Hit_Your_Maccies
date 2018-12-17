from django.shortcuts import render
from django.http import HttpResponse
from .models import Food
from .forms import CalcuFilter


def process_food(food, protein_required):
    
    protein = float(food.pro)
    if protein < 0.01:
        return 0

    if protein > protein_required:
        quantity = 1 
    else:
        quantity = int(protein_required / protein)

    return quantity



def index(request):

    if request.method == 'POST':
        get = False
        protein = request.POST['pro']
        category = request.POST['category']
        foods = Food.objects.order_by('pro')
        if category != 'ALL':
            foods = foods.filter(category=category)

        foods = list(foods) # force evaluation of queryset to allow extra attributes to be set
        for food in foods:
            food.quantity = process_food(food, float(protein))



        form = CalcuFilter(request.POST)

        if form.is_valid():
            pass #trigger validation
        


    else:
        form = CalcuFilter()
        foods = Food.objects.order_by('-cal')[:1]
        get = True

    context = {'foods': foods,
                'form': form,
                'get': get}

    
    

    return render(request, 'calculator/index.html', context)



def about(request):
    context = {}
    return render(request, 'calculator/about.html', context)


def contact(request):
    context = {}
    return render(request, 'calculator/contact.html', context)