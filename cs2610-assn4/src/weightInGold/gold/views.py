from django.shortcuts import render

from unitconv.models import ConversionUnit


def plan(request):
    return render(request, 'gold/plan.html')

def index(request):
    
    convUnits = ConversionUnit.objects.all()
    validUnits = []
    for convUnit in convUnits:
        validUnits.append(convUnit.unit)
   
    context = {'validUnits': validUnits}
    return render(request, 'gold/index.html', context=context)

