from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from tc.models import Subsystem

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class SubsystemForm(forms.ModelForm):
    class Meta:
        model = Subsystem
        fields = ['button_value']