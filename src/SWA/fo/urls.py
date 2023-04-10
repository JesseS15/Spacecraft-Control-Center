from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
 
app_name = 'fo'
urlpatterns = [
    path('home/', views.foHome, name ='home'),
    path('join/', views.joinClass, name ='join'),
    path('home/<str:class_name>', views.foClass, name ='classHome'),
    path('<int:simkey>/acs/', views.acs, name ='acs'),
    path('<int:simkey>/eps/', views.eps, name ='eps'),
    path('<int:simkey>/tcs/', views.tcs, name ='tcs'),
    path('<int:simkey>/payload/', views.payload, name ='payload'),
    path('<int:simkey>/comms/', views.comms, name ='comms'),
    path('<int:simkey>/acs/fetchdata/', views.fetchdata, name='fetchdata'),
    path('<int:simkey>/eps/fetchdata/', views.fetchdata, name='fetchdata'),
    path('<int:simkey>/tcs/fetchdata/', views.fetchdata, name='fetchdata'),
    path('<int:simkey>/payload/fetchdata/', views.fetchdata, name='fetchdata'),
    path('<int:simkey>/comms/fetchdata/', views.fetchdata, name='fetchdata'),
    path('<int:simkey>/acs/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/eps/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/tcs/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/payload/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/comms/fetchcommands/', views.fetchcommands, name='fetchcommands'),
    path('<int:simkey>/submit', views.submit, name='submit'),
    path('<int:simkey>/sim', views.sim, name ='sim'),
]