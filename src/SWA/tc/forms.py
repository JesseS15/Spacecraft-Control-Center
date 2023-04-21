from django import forms
import re
import random
import string
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from fo.models import FlightOperator
from simapp.models import Sim, Mission
from .models import Class, TestConductor
 
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
    class_name = forms.CharField(initial='') 
    
    #def clean_msg(self):
     #   class_name = self.cleaned_data['class_name']
      ##     raise ValidationError("Spaces not allowed")
       # return class_name
    missions = forms.ModelMultipleChoiceField(queryset=Mission.objects, help_text=("Hold Ctrl to Select Multiple"), required = False)
    test = True
    class Meta:
        model = Class
        fields = ['class_name','status','missions','sims','test']
        widgets = {'test': forms.HiddenInput(), 'status': forms.HiddenInput(), 'sims':forms.HiddenInput(),}

###############################################################################
class SimCreationForm(forms.ModelForm):
    sim_name = forms.CharField(required=True, initial='')

    def __init__(self, class_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_class = Class.objects.get(class_name=class_name)
        flight_operators = selected_class.flight_operators.all()

        self.fields['mission_script'] = forms.ModelChoiceField(queryset=selected_class.missions, required=True)
        self.fields['flight_director'] = forms.ModelChoiceField(queryset=flight_operators, required=True)
        self.fields['COMMS_fo'] = forms.ModelChoiceField(queryset=flight_operators, required=True)
        self.fields['ACS_fo'] = forms.ModelChoiceField(queryset=flight_operators, required=True)
        self.fields['EPS_fo'] = forms.ModelChoiceField(queryset=flight_operators, required=True)
        self.fields['TCS_fo'] = forms.ModelChoiceField(queryset=flight_operators, required=True)
        
    class Meta:
        model = Sim
        fields = ['sim_name', 'status', 'mission_script', 'flight_director', 'COMMS_fo', 'ACS_fo', 'EPS_fo', 'TCS_fo']
        widgets = {'status': forms.HiddenInput()}
    
        #FlightOperator.objects.filter(user_class_list__icontains=class_name).values()
###################################################################3
class MissionCreationForm(forms.ModelForm):
    mission_name = forms.CharField(max_length = 20)
    
    class Meta:
        model = Mission
        fields = ['mission_name', 'final_roll', 'final_pitch', 'final_yaw']

################################################################
class ClassEditForm(forms.ModelForm):
    test = False
    randomizecode = forms.BooleanField(initial = False, required=False, label="Randomize Code")
    #test = forms.BooleanField(widget=forms.HiddenInput(), initial=False)
    #status = forms.CharField(widget=forms.HiddenInput(), initial=Class.status) 
    code  = forms.CharField(initial='', required=False)
    missions = forms.ModelMultipleChoiceField(queryset=Mission.objects, help_text=("Hold Ctrl to Select Multiple"), required = False)
    delete = forms.BooleanField(initial = False, required=False)
    class Meta:
        model = Class
        fields = ['randomizecode','code']
        widgets = {'status': forms.HiddenInput()}
######################################################
class SimEditForm(forms.ModelForm):
    test = False
    delete = forms.BooleanField(initial = False, required=False)
    #test = forms.BooleanField(widget=forms.HiddenInput(), initial=False)
    #status = forms.CharField(widget=forms.HiddenInput(), initial=Class.status) 
    class Meta:
        model = Sim
        fields = []
        widgets = {'status': forms.HiddenInput()}

############################################################
class MissionEditForm(forms.ModelForm):
    delete = forms.BooleanField(initial = False, required=False)
    #test = forms.BooleanField(widget=forms.HiddenInput(), initial=False)
    #status = forms.CharField(widget=forms.HiddenInput(), initial=Class.status) 
    class Meta:
        model = Mission
        fields = []
        
