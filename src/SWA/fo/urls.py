from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
 
urlpatterns = [
    path('', views.Login, name ='login'),
    path('', views.Login, name ='foLogin'),
    path('foHome/', views.foHome, name ='foHome'),
    path('foProfile/', views.foProfile, name='foProfile'),
    path('logout', views.Logout, name ='foLogout'),
    path('foRegister/', views.register, name ='foRegister'),
]