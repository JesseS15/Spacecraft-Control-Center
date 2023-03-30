from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from fo.models import FlightOperator
from simapp.models import Subsystem, Sim, Mission
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
    test = True
    class Meta:
        model = Class
        fields = ['class_name','status','sims', 'test']
        widgets = {'test': forms.HiddenInput(), 'status': forms.HiddenInput()}

###############################################################################
class SimCreationForm(forms.ModelForm):

    #flight_director = forms.ModelChoiceField(queryset=None)
    #flight_director = forms.MultipleChoiceField(widget=forms.SelectMultiple,label="Select the devices you want to delete:")
    def __init__(self, class_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #test = Class.objects.all().filter(class_name = class_name).values_list("flight_operators__user__username", flat="True")

        testa = Class.objects.get(class_name = class_name)
        test = testa.flight_operators.all()
        missionA = TestConductor.objects.get().missions.all()

        self.fields['mission_script'].queryset = missionA
        self.fields['flight_director'].queryset = test
        self.fields['COMMS_fo'].queryset = test
        self.fields['ACS_fo'].queryset = test
        self.fields['EPS_fo'].queryset = test
        self.fields['TCS_fo'].queryset = test
        #self.test = test
   
    #flight_director = forms.MultipleChoiceField(widget=forms.SelectMultiple,label="Select the devices you want to delete:", choices = test)

    class Meta:
        model = Sim
        fields = ['sim_name', 'mission_script', 'flight_director', 'COMMS_fo','ACS_fo', 'EPS_fo', 'TCS_fo']
    
        #FlightOperator.objects.filter(user_class_list__icontains=class_name).values()
###################################################################3
class MissionCreationForm(forms.ModelForm):
    mission_name = forms.CharField(max_length = 20)

    class Meta:
        model = Mission
        fields = ['mission_name', 'final_roll', 'final_pitch', 'final_yaw', 'start_longitude', 'final_longitude']

class SubsystemForm(forms.Form):
    sys_name = forms.CharField(max_length=15)
################################################################
class ClassEditForm(forms.ModelForm):
    test = False
    delete = forms.BooleanField(initial = False, required=False)
    #test = forms.BooleanField(widget=forms.HiddenInput(), initial=False)
    #status = forms.CharField(widget=forms.HiddenInput(), initial=Class.status) 
    #code  = forms.CharField(widget=forms.HiddenInput(), initial=123)
    class Meta:
        model = Class
        fields = ['status','code']
        widgets = {'status': forms.HiddenInput()}
