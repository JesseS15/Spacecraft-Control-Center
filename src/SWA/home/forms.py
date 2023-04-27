# STaTE
# File: home/forms.py
# Purpose: This file defines forms for user-provided data submission in the home Django app

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

###############################################################################
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']