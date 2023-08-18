from django.urls import path

from . import views

app_name='gold'
urlpatterns=[
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('plan.html', views.plan, name='plan'),
]
