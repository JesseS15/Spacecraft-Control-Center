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
    path('<str:simkey>/acs/', views.acs, name ='acs'),
    path('<str:simkey>/eps/', views.eps, name ='eps'),
    path('<str:simkey>/acs/fetchdata/', views.fetchdata, name='fetchdata'),
    path('<str:simkey>/eps/fetchdata/', views.fetchdata, name='fetchdata'),
    path('<str:simkey>/submit', views.submit, name='submit'),
]