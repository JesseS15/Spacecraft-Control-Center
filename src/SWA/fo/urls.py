from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
 
urlpatterns = [
    path('', views.Login, name ='login'),
    path('foHome/', views.foHome, name ='foHome'),
    path('', auth.LogoutView.as_view(template_name ='fo/index.html'), name ='logout'),
    path('register/', views.register, name ='register'),
]