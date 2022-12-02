from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
 
app_name = 'fo'
urlpatterns = [
    path('', views.index, name ='index'),
    path('login/', views.foLogin, name ='login'),
    path('logout/', views.foLogout, name ='logout'),
    path('register/', views.foRegister, name ='register'),
    path('home/', views.foHome, name ='home'),
    path('<str:sim>/', views.foSim, name ='sim'),
]