from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
 
urlpatterns = [
    path('', views.Login, name ='login'),
    path('', views.Login, name ='tcLogin'),
    path('tcHome/', views.getGroups, name ='tcHome'),    
    path('', auth.LogoutView.as_view(template_name ='tc/index.html'), name ='logout'),
    path('register/', views.register, name ='register'),
    path('logout', views.Logout, name ='logout'),
    path('addClass/', views.addClass, name ='addClass'),
    path('classHome/', views.classHome, name='classHome')
]