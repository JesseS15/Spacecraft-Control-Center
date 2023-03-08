from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from fo.models import FlightOperator
from simapp.models import Subsystem, Sim
from .models import Class, Sim
 
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

    flight_dir = forms.SelectMultiple()
    class Meta:
        model = Sim
        fields = ['sim_name', 'flight_director', 'COMMS_fo', 'ACS_fo', 'TCS_fo', 'EPS_fo']

    def __init__(self, class_name, *args, **kwargs):
        super(SimCreationForm, self).__init__(*args, **kwargs)
        test = Class.objects.all().filter(class_name = class_name).values_list("flight_operators__user__username", flat="True")
        self.fields['flight_director'].queryset = test
    def __init__(self, class_name, *args, **kwargs):
        super(SimCreationForm, self).__init__(*args, **kwargs)
        test = Class.objects.all().filter(class_name = class_name).values_list("flight_operators__user__username", flat="True")
        self.fields['COMMS_fo'].queryset = test
    def __init__(self, class_name, *args, **kwargs):
        super(SimCreationForm, self).__init__(*args, **kwargs)
        test = Class.objects.all().filter(class_name = class_name).values_list("flight_operators__user__username", flat="True")
        self.fields['ACS_fo'].queryset = test
    def __init__(self, class_name, *args, **kwargs):
        super(SimCreationForm, self).__init__(*args, **kwargs)
        test = Class.objects.all().filter(class_name = class_name).values_list("flight_operators__user__username", flat="True")
        self.fields['EPS_fo'].queryset = test
    def __init__(self, class_name, *args, **kwargs):
        super(SimCreationForm, self).__init__(*args, **kwargs)
        test = Class.objects.all().filter(class_name = class_name).values_list("flight_operators__user__username", flat="True")
        self.fields['TCS_fo'].queryset = test
        #FlightOperator.objects.filter(user_class_list__icontains=class_name).values()


###################################################################3
class MissionCreationForm(forms.Form):
    mission_name = forms.CharField(max_length = 20)
    
class SubsystemForm(forms.Form):
    sys_name = forms.CharField(max_length=15)