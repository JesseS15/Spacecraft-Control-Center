from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from simapp.models import Subsystem

###############################################################################
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

###############################################################################
class JoinClassForm(forms.Form):
    code = forms.CharField(max_length = 8)
    fields = ['code']