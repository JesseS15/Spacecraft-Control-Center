from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth

app_name = 'tc'
urlpatterns = [
    path('', views.index, name ='index'),
    path('login/', views.tcLogin, name ='login'),
    path('logout/', views.tcLogout, name ='logout'),
    path('register/', views.tcRegister, name ='register'),
    path('home/', views.tcHome, name ='home'),
    path('addClass/', views.addClass, name ='addClass'),
    path('classHome/', views.classHome, name='classHome'),
    path('create/', views.createSim, name='createSim'),
    path('<str:sim>/', views.tcSim, name ='sim'),
]