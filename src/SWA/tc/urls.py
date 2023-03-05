from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth

app_name = 'tc'
urlpatterns = [
    path('', views.index, name ='index'),
    path('home/', views.tcHome, name ='home'),
    path('home/<str:class_name>/newMission', views.newMission, name='new'),
    path('home/<str:class_name>/newSim', views.newSim, name='new'),
    #path('addClass/', views.addClass, name ='addClass'),# ##unused because moved##
    path('home/<str:class_name>', views.classHome, name='classHome'),
    #path('create/<str:class_name>', views.createSim, name='createSim'),# ##unused because moved##
    path('<str:sim>/', views.tcSim, name ='sim'),
    
]