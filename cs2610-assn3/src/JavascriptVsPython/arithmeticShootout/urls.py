from django.urls import path

from .import views

urlpatterns = [
    path('', views.index, name='calculator'),
    path('index.html', views.index, name='calculator'),
    path('recent.html', views.recent, name='recent'),
    path('undefined.html', views.undefined, name='undefined'),
    path('disagreeing.html', views.disagreeing, name='disagreeing'),
    path('operator.html', views.operator, name='operator'),
    path('plan.html', views.plan, name='plan'),
    path('addExpression', views.addExpression, name='addExpression'),
    path('removeExpression', views.removeExpression, name='removeExpression'),
]

