from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('archive.html', views.archive, name='archive'),
    path('<int:blog_id>/', views.detail, name='detail'),
    path('about.html', views.about, name='about'),
    path('techtips-css.html', views.techtipsWithoutCss, name='techtips-without-css'),
    path('techtips+css.html', views.techtipsWithCss, name='techtips-with-css'),
    path('plan.html', views.plan, name='plan'),
]

