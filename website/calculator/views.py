from django.shortcuts import render
from django.http import HttpResponse
from .models import Food
from .forms import CalcuFilter

def index(request):
    foods = Food.objects.order_by('-cal')[:5]

    if request.method == 'POST':
        form = CalcuFilter(request.POST)
        if form.is_valid():
            pass #trigger validation
    else:
        form = CalcuFilter()

    context = {'foods': foods,
                'form': form}
    return render(request, 'calculator/index.html', context)






def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'home.html', {'form': form})