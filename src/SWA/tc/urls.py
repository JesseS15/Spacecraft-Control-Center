from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
from simapp import views as simappViews

app_name = 'tc'
urlpatterns = [
    path('', views.index, name ='index'),
    path('home/', views.tcHome, name ='home'),
    path('home/<str:class_name>/newMission', simappViews.newMission, name='newMission'),
    path('home/<str:class_name>/newSim', simappViews.newSim, name='newSim'),
    path('home/<str:class_name>', views.classHome, name='classHome'),
    path('<int:simkey>/', views.tcSim, name ='sim'),
]