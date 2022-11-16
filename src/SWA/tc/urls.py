from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='tclogin'),
    path('createSim/', views.createSim, name='createSim'),
]