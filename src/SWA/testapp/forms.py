from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from simapp.models import Sim

###############################################################################
class SimForm(forms.Form):

    sim_name = forms.CharField(max_length = 20)

###################################################################3
class MissionCreationForm(forms.Form):
    mission_name = forms.CharField(max_length = 20)
