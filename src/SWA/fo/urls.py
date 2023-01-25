from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
 
app_name = 'fo'
urlpatterns = [
    path('', views.index, name ='index'),
    path('home/', views.foHome, name ='home'),
    path('join/', views.joinClass, name ='join'),
    path('<str:sim>/', views.foSim, name ='sim'),
]