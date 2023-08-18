from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db import models

from .models import Operator, Expression

def index(request):
    
    operators = Operator.objects.order_by('id')[:6] 
    latest_expressions = Expression.objects.order_by('-id')[:5]
    context = {'operators': operators, 'latest_expressions': latest_expressions}
    return render(request, 'arithmeticShootout/calculator.html', context)


def recent(request):
    saved_expressions = Expression.objects.order_by('-id')[:]
    context = {'saved_expressions': saved_expressions}
    return render(request, 'arithmeticShootout/recent.html', context)


def undefined(request):
    undefined_expressions = Expression.objects.filter(defined=False)
    context = {'undefined_expressions': undefined_expressions}
    return render(request, 'arithmeticShootout/undefined.html', context)


def disagreeing(request):
    disagreeing_expressions = Expression.objects.filter(agree=False)
    context = {'disagreeing_expressions': disagreeing_expressions}
    return render(request, 'arithmeticShootout/disagreeing.html', context)


def operator(request):
    all_expressions = Expression.objects.all()
    add_expressions = []
    sub_expressions = []
    mul_expressions = []
    div_expressions = []
    rem_expressions = []
    exp_expressions = []
    for expression in all_expressions:
      if expression.operator.symbol == "+":
          add_expressions.append(expression)

      if expression.operator.symbol == "-":
          sub_expressions.append(expression)

      if expression.operator.symbol == "*":
          mul_expressions.append(expression)

      if expression.operator.symbol == "/":
          div_expressions.append(expression)

      if expression.operator.symbol == "%":
          rem_expressions.append(expression)

      if expression.operator.symbol == "**":
          exp_expressions.append(expression)
    
    context = {'add_expressions': add_expressions, 'sub_expressions': sub_expressions, 'mul_expressions': mul_expressions, 'div_expressions': div_expressions, 'rem_expressions': rem_expressions, 'exp_expressions': exp_expressions}
    return render(request, 'arithmeticShootout/operator.html', context)


def plan(request):
    return render(request, 'arithmeticShootout/plan.html')


def addExpression(request):
   # When the save button created in the form our js made is pressed, this gets called.
   if request.POST:

       tempOps = Operator.objects.all()
       operators = []
       for operator in tempOps:
           operators.append(operator.symbol)         

       if (not (request.POST['operator'].split()[0] in operators)):
           print("Bad Operator")
           return render(request, 'arithmeticShootout/error.html')

       try:

           operand1 = float(request.POST['op1'])
           operatorArr = request.POST['operator'].split()
           operator = Operator(symbol=operatorArr[0], name=operatorArr[1])
           operand2 = float(request.POST['op2'])
           result = request.POST['result']
           pyresult = float("NaN")
           defined = True
           agree = True

           if result == 'undefined':
               defined = False
               result = float("NaN")
           
           else:
               result = float(result)
         
           if (defined):
               pyresult = eval(f"{operand1} {operator.symbol} {operand2}")
               agree = (result == pyresult)

       except Exception as e: 
           print(f"{e}\nBad Operand or the likes")
           return render(request, 'arithmeticShootout/error.html')
       
       else:
           operator.save()
           expression = Expression(operand1=operand1, operator=operator, operand2=operand2, defined=defined, result=result, agree=agree, pyresult=pyresult)
           
           print(expression.id)
           expression.save()  
           print(expression.id)         
 
           if "HTTP_REFERER" in request.META:
               return HttpResponseRedirect(request.META["HTTP_REFERER"])
           else:
               return HttpResponseReidrect('arithmeticShootout/calculator.html')

   return render(request, 'arithmeticShootout/calculator.html')


def removeExpression(request):
    # When the delete button of a saved expression gets pressed, this gets called.
    if request.POST:
        # Get the object id and deletes it from the database.
        print(request.POST['id'])    
        expression = Expression.objects.get(pk=request.POST['id'])
        expression.delete()
    
    if "HTTP_REFERER" in request.META:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    
    return HttpResponseRedirect('arithmeticShootout/calculator.html') 

