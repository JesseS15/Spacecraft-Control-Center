from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
 
urlpatterns = [
    path('', views.Login, name ='foLogin'),
    path('foHome/', views.foHome, name ='foHome'),
    path('logout', views.Logout, name ='foLogout'),
    path('register/', views.register, name ='register'),
]