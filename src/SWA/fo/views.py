from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.template import loader
from .models import FlightOperator
  
#################### index#######################################
def index(request):
    return render(request, 'fo/foIndex.html', {'title':'index'})
  
########### register here #####################################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            ######################### mail system ####################################
            send_mail(
                'STaTE Registration',
                'Thank you for registering to STaTE!',
                None,
                [email],
                fail_silently=False,
            )
            ##################################################################
            user = authenticate(request, username = username, password = password)
            form = login(request, user)
            FlightOperator.objects.create(user = user)
            return redirect('foHome')
    else:
        form = UserRegisterForm()
    return render(request, 'fo/foRegister.html', {'form': form, 'title':'register here'})
  
################ login forms###################################################
def Login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None and user.is_staff:
            #messages.info(request, f'Information submitted is for a Test Conductor account. Redirecting to Test Conductor login.')
            return redirect('tcLogin')
        if user is not None and not user.is_staff:
            form = login(request, user)
            #messages.success(request, f' welcome {username} !!')
            return redirect('foHome')
        else:
            messages.info(request, f'account does not exist')

    elif request.user.is_authenticated:
        return redirect('foHome')

    form = AuthenticationForm()
    return render(request, 'fo/foLogin.html', {'form':form, 'title':'log in'})

################ logout method###################################################
def Logout(request):

    logout(request)
    return Login(request)

def foHome(request):

    flightOperator = None
    for fo in FlightOperator.objects.all():
        if fo.user == request.user:
            flightOperator = fo

    return render(request, 'fo/foHome.html', {'user':request.user, 'flightOperator':flightOperator})

def foProfile(request):
    flightOperator = None
    for fo in FlightOperator.objects.all():
        if fo.user == request.user:
            flightOperator = fo
    return render(request, 'fo/foProfile.html', {'user':request.user, 'flightOperator':flightOperator})