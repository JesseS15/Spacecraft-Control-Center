# STaTE
# File: home/urls.py
# Purpose: This file defines url patterns to route user http requests in the home Django app

from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.userLogin, name ='login'),
    path('logout/', views.userLogout, name ='logout'),
    path('register/', views.register, name ='register'),
]