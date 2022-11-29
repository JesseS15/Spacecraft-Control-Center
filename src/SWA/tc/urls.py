from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
 
urlpatterns = [
    path('', views.Login, name ='tcLogin'),
    path('tcHome/', views.tcHome, name ='tcHome'),
    path('', auth.LogoutView.as_view(template_name ='tc/index.html'), name ='logout'),
    path('register/', views.register, name ='register'),
]