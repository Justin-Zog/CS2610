from django.shortcuts import render
from django.http import JsonResponse

from .models import ConversionUnit


def index(request):
    return render(request, 'unitconv/index.html')


def convertAnything(from_unit, to_unit, value):
    # Takes two conversion units and converts accordingly.
    # To do this we divide value by from's conversion_factor to get it in troy ounces
    # Then we multiply the result by to's conversion_factor to get it into that unit instead of troy_ounces
    step1 = value / from_unit.conversion_factor
    result = step1 * to_unit.conversion_factor
    return result


def convert(request):
    # Gets our valid conversion units
    convUnits = ConversionUnit.objects.all()
    validUnits = []
    for convUnit in convUnits:
        validUnits.append(convUnit.unit)

    # Checks to see that all our get parameters are here.
    if 'to' not in request.GET or 'from' not in request.GET or 'value' not in request.GET:    
        resp = {'error': "GET is missings one or more parameters! Usage: ?from=<unit1>&to=<unit2>&value=<positive number>", 'success': False }
    # Checks to see that our values are valid.
    elif not request.GET['value'].replace(".", "", 1).isdigit():
        resp = {'error': "value must be a positive number not a word or something else. Try again.", 'success': False }
    elif float(request.GET['value']) < 0:
        resp = {'error': "value must be a positive number. Try again.", 'success': False }
    elif not request.GET['from'] in validUnits or not request.GET['to'] in validUnits:
        resp = {'error': "to and from must be valid units of measure or the program doesn't recognize the unit that you input. Try again."}
    else: 
        from_unit = convUnits.filter(unit=request.GET['from']).first()
        to_unit = convUnits.filter(unit=request.GET['to']).first()
        initialValue = float(request.GET['value'])

        value = convertAnything(from_unit, to_unit, initialValue)
        resp = {'units': to_unit.unit, 'value': value, 'success': True }

    return JsonResponse(resp)
