from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from fo.models import FlightOperator
from simapp.models import Subsystem, Sim
from .models import Class
 
 ###############################################################################
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

###############################################################################
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name','status','sims']

###############################################################################
class SimCreationForm(forms.ModelForm):
    class Meta:
        model = Sim
        fields = ['sim_name', 'flight_operators']

###################################################################3
class MissionCreationForm(forms.Form):
    mission_name = forms.CharField(max_length = 20)
    
class SubsystemForm(forms.Form):
    sys_name = forms.CharField(max_length=15)