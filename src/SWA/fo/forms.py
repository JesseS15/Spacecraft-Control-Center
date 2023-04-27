# STaTE
# File: fo/forms.py
# Purpose: This file defines forms for user-provided data submission in the fo Django app

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

###############################################################################
class JoinClassForm(forms.Form):
    code = forms.CharField(max_length = 8)
    fields = ['code']