from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
 
app_name = 'fo'
urlpatterns = [
    path('home/', views.foHome, name ='home'),
    path('join/', views.joinClass, name ='join'),
    path('<str:simkey>/', views.foSim, name ='sim'),
    path('<str:simkey>/fetchdata/', views.fetchdata, name='fetchdata'),
    path('<str:simkey>/submit/', views.submit, name='submit'),
]