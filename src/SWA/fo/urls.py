# STaTE
# File: fo/urls.py
# Purpose: This file defines url patterns to route user http requests in the fo Django app

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth
from django.urls import path, include
 
app_name = 'fo'
urlpatterns = [
    path('home/', views.foHome, name ='home'),
    path('join/', views.joinClass, name ='join'),
    path('home/<str:class_name>', views.foClass, name ='classHome'),
    path('<int:simkey>/acs/', views.acs, name ='acs'),
    path('<int:simkey>/eps/', views.eps, name ='eps'),
    path('<int:simkey>/tcs/', views.tcs, name ='tcs'),
    path('imagedisplay/', views.imagedisplay, name ='imagedisplay'),
    path('rickroll/', views.rickdisplay, name='rickroll'),
    path('<int:simkey>/payload/', views.payload, name ='payload'),
    path('<int:simkey>/comms/', views.comms, name ='comms'),
    path('<int:simkey>/acs/fetchdata/', views.acsFetchdata, name='acsFetchdata'),
    path('<int:simkey>/eps/fetchdata/', views.epsFetchdata, name='epsFetchdata'),
    path('<int:simkey>/tcs/fetchdata/', views.tcsFetchdata, name='tcsFetchdata'),
    path('<int:simkey>/payload/fetchdata/', views.payloadFetchdata, name='payloadFetchdata'),
    path('<int:simkey>/comms/fetchdata/', views.commsFetchdata, name='commsFetchdata'),
    path('<int:simkey>/acs/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/eps/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/tcs/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/payload/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/comms/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/submit', views.submit, name='submit'),
    path('<int:simkey>/sim', views.sim, name ='sim'),
]