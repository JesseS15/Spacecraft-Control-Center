from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='tcLogin'),
    path('createSim/', views.createSim, name='createSim'),
]