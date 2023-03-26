import numpy
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
import time
from .models import Class

from .models import TestConductor, Class
from simapp.models import Sim, Subsystem, Mission
from .forms import UserRegisterForm, SimCreationForm, ClassForm, MissionCreationForm, SubsystemForm


###############################################################################
def index(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('tc:home')
    else:
        return redirect('home:login')

###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def tcHome(request):
    classes = Class.objects.all()
    
    if not TestConductor.objects.filter(user = request.user).exists():
        TestConductor.objects.create(user = request.user).save()

    print(classes)
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            start = time.time()
            form.save()
            duration = (time.time() - start) * 1000
            print('form.name {:.2f} ms'.format(
            duration
            ))
            return redirect('tc:home')
    else:
        form = ClassForm()

    return render(request, 'tc/tcHome.html', {"classes":classes, 'form': form})
  
###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def classHome(request, class_name):

    group = Class.objects.all().filter(class_name = class_name).values_list('sims', flat=True)
    data = numpy.asarray(group)
    print(group)
    if (data.all()!=None):
        sims = ['']*(len(data))
        for e in range(len(data)):
            print(Sim.objects.get(pk=data[e]))
            sims[e] = Sim.objects.get(pk=data[e])
        print(sims)
    else:
        sims=[]
    #############################################################################
    group2 = TestConductor.objects.all().values_list('missions', flat=True)
    data2 = numpy.asarray(group2)
    print(group2)
    if (data2.all()!=None):
        missions = ['']*(len(data2))
        for e in range(len(data2)):
            print(Mission.objects.get(pk=data2[e]))
            missions[e] = Mission.objects.get(pk=data2[e])
        print(missions)
    else:
        missions=[] 
    ###############################################################################
    """if request.method == 'POST':
        form = SimCreationForm(request.POST)

        if form.is_valid():
            sim_list = form.cleaned_data.get('sim_list')
            sim_name = form.cleaned_data.get('sim_name')
            sys_list = form.cleaned_data.get('sys_list')
            flight_operators = form.cleaned_data.get('flight_operators')

            sim = Sim.objects.create(sim_name = sim_name)
            Class.objects.get(class_name = class_name).sims.add(sim)
            for x in sys_list:
                sim.sys_list.add(x)
                #sys_list.sim_list.add(sim)
                #class_belong.sim_list.add(sim)
            #form.save_m2m()
            ##gohere
            for flight_operator in flight_operators:
                sim.flight_operators.add(flight_operator)
                #flight_operator.sim_list.add(sim)
                # Send notification
                send_mail(
                    'STaTE Simulation Added to Your Account',
                    'A new simulation, ' + sim.sim_name + ', has been added to your STaTE account.',
                    None,
                    [flight_operator.user.email],
                    fail_silently=False,
                )
                return redirect('tc:home/class_name')
            

    form = SimCreationForm()"""
    # 3/5/23 Removed "missions":missions
    return render(request, 'tc/classHome.html', {"class_name": class_name, "sims":sims, "missions":missions})

###############################################################################
def getGroups(request):
    
    group = list(request.user.groups.values_list('name', flat = True))
    data = numpy.asarray(group)
    print(data) 
    return render(request, 'tc: home.html', {"data":data})

###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def tcSim(request, sim):
    simobj = Sim.objects.get(sim_name=sim)

    if request.method == 'POST':

        for subsystem in simobj.sys_list.all():
            if subsystem.sys_name in request.POST:
                form = SubsystemForm(request.POST, prefix=subsystem.sys_name, instance=subsystem)
                if form.is_valid():
                    #form.save_m2m()
                    form.save()
                    for flight_operator in simobj.flight_operators.all():
                        # Send notification
                        send_mail(
                            'STaTE: ' + sim,
                            'An anomoly has occured on your SimCraft: ' + sim + '.',
                            None,
                            [flight_operator.user.email],
                            fail_silently=False,
                        )
    print(simobj)
    forms = [SubsystemForm(prefix=subsystem.sys_name, instance=subsystem) for subsystem in simobj.sys_list.all()]
    return render(request, 'tc/tcSim.html', {'sim': simobj, 'forms': forms})
