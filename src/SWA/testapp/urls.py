from django.urls import path

from . import views

app_name = 'testapp'
urlpatterns = [
    path('home/', views.testappHome, name ='home'),
    path('home/newSim', views.newSim, name ='newSim'),
    path('home/newMission', views.newMission, name ='newMission'),
    path('<str:simkey>/', views.testappSim, name ='sim'),
    path('<str:simkey>/fetchdata/', views.fetchdata, name='fetchdata'),
    path('<str:simkey>/submit', views.submit, name='submit'),
]