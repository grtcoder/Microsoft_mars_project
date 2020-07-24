 
from django.urls import path
from . import views
from django.shortcuts import render, redirect
urlpatterns = [
    path('',views.home,name='home'),
    path('common',views.common,name='common'),
    path('tsp',views.tsp,name='tsp'),
    path('common/api',views.test,name='api'),
    path('tsp/tspapi',views.tspapi,name='tspapi')
]
