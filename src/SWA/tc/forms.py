from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from fo.models import FlightOperator
from simapp.models import Subsystem
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
        # 3/5/23 Removed 'mission' so it was not required
        fields = ['class_name','status','sims']

###############################################################################
class SimCreationForm(forms.Form):

    sim_name = forms.CharField(max_length = 20)

    flight_operators = forms.ModelMultipleChoiceField(
        queryset=FlightOperator.objects.all(),
        widget=forms.CheckboxSelectMultiple, blank=True)
    #sys_list = forms.ModelMultipleChoiceField(
    #    queryset=Subsystem.objects.all(),
    #    widget=forms.CheckboxSelectMultiple)
###################################################################3
class MissionCreationForm(forms.Form):
    mission_name = forms.CharField(max_length = 20)
    
class SubsystemForm(forms.Form):
    sys_name = forms.CharField(max_length=15)