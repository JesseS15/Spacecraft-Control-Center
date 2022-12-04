from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from fo.models import FlightOperator
 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class GroupRegisterForm(forms.ModelForm):
    name = forms.CharField(max_length = 20)
    status = forms.CharField(max_length = 20)
    class Meta:
        model = Group
        fields = ['name','status']

class SimCreationForm(forms.Form):
    sim_name = forms.CharField(max_length = 20)
    sys1_name = forms.CharField(max_length = 20)
    sys2_name = forms.CharField(max_length = 20)
    sys3_name = forms.CharField(max_length = 20)

    flight_operators = forms.ModelMultipleChoiceField(
        queryset=FlightOperator.objects.all(),
        widget=forms.CheckboxSelectMultiple)