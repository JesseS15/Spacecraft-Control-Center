# STaTE
# File: tc/urls.py
# Purpose: This file defines url patterns to route user http requests in the tc Django app

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth
from django.urls import path, include

from . import views
from simapp import views as simappViews

app_name = 'tc'
urlpatterns = [
    path('', views.index, name ='index'),
    path('home/', views.tcHome, name ='home'),
    path('home/downloadSimReport/', views.downloadSimReport, name='downloadSimReport'),
    path('home/<str:class_name>/newMission', simappViews.newMission, name='newMission'),
    path('home/<str:class_name>/newSim', simappViews.newSim, name='newSim'),
    path('home/<str:class_name>', views.classHome, name='classHome'),
    path('<int:simkey>/', views.tcSim, name ='sim'),
    path('<int:simkey>/acs/', views.acs, name ='acs'),
    path('<int:simkey>/eps/', views.eps, name ='eps'),
    path('<int:simkey>/tcs/', views.tcs, name ='tcs'),
    path('<int:simkey>/payload/', views.payload, name ='payload'),
    path('<int:simkey>/comms/', views.comms, name ='comms'),
    path('<int:simkey>/acs/fetchdata/', views.acsFetchdata, name='acsFetchdata'),
    path('<int:simkey>/eps/fetchdata/', views.epsFetchdata, name='epsFetchdata'),
    path('<int:simkey>/tcs/fetchdata/', views.tcsFetchdata, name='tcsFetchdata'),
    path('<int:simkey>/payload/fetchdata/', views.payloadFetchdata, name='payloadFetchdata'),
    path('<int:simkey>/comms/fetchdata/', views.commsFetchdata, name='commsFetchdata'),
]