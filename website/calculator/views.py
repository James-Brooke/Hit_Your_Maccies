from django.shortcuts import render
from django.http import HttpResponse
from .models import Food
from .forms import CalcuFilter

def index(request):

    protein = None

    if request.method == 'POST':
        get = False
        protein = request.POST['pro']

        foods = Food.objects.filter(pro__gte=protein).order_by('pro')
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
    if protein:
        context['protein'] = protein
    
    

    return render(request, 'calculator/index.html', context)






def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'home.html', {'form': form})