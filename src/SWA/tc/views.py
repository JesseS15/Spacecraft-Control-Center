import numpy
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, GroupRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

from .models import TestConductor, Sim

###############################################################################
def index(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('tc:home')
    else:
        return redirect('tc:login')
  
###############################################################################
def tcRegister(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            # Send registration confirmation
            send_mail(
                'STaTE Registration',
                'Thank you for registering to STaTE!',
                None,
                [email],
                fail_silently=False,
            )
            user = authenticate(request, username = username, password = password)
            form = login(request, user)
            TestConductor.objects.create(user = user)
            return redirect('tc:home')
    else:
        form = UserRegisterForm()

    return render(request, 'tc/register.html', {'form': form, 'title':'register here'})
  
###############################################################################
def tcLogin(request):      

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None and not user.is_staff:
            return redirect('fo:login')
        if user is not None and user.is_staff:
            form = login(request, user)
            return redirect('tc:home')
        else:
            messages.info(request, f'account does not exist')

    elif request.user.is_authenticated and not request.user.is_staff:
        return redirect('tc:home')

    form = AuthenticationForm()
    return render(request, 'tc/login.html', {'form':form, 'title':'log in'})

###############################################################################
def tcLogout(request):
    logout(request)
    return redirect('tc:login')

###############################################################################
def tcHome(request):
    group = list(request.user.groups.values_list('name', flat = True))
    data = numpy.asarray(group)
    print(data) 
    return render(request, 'tc/tcHome.html', {"data":data})
  
###############################################################################
def classHome(request):
    return render(request, 'tc/classHome.html')

###############################################################################
def getGroups(request):
    
    group = list(request.user.groups.values_list('name', flat = True))
    data = numpy.asarray(group)
    print(data) 
    return render(request, 'tc: home.html', {"data":data})

###############################################################################
def createSim(request):
    template = loader.get_template('tc/createSim.html')
    context = {}
    return HttpResponse(template.render(context, request))

#############get group names#######################

def addClass(request):
    if request.method == 'POST':
        form = GroupRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            group = request.POST['name']
            print(group)
            my_group = Group.objects.get(name=group) 
            my_group.user_set.add(request.user)
            name = form.cleaned_data.get('name')
            status = form.cleaned_data.get('status')
            ##group = authenticate(request, name = name, status = status)
            ##Classes.objects.create(group = group)
            return redirect('tc:home')
    else:
        form = GroupRegisterForm()
    return render(request, 'tc/addClass.html', {'form': form, 'title':'Add Class'})

###############################################################################
def tcSim(request, sim):
    #simobj = Sim.objects.get(sim_name=sim)

    return render(request, 'tc/tcHome.html')