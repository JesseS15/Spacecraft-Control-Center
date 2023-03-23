from django.contrib import messages
import numpy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SimForm, MissionCreationForm

from .models import Sim, DisplayBufferItem, Mission

from tc.models import TestConductor, Class

from django.http import JsonResponse
from django.template.loader import render_to_string
import json

from simulation.SimObject import SimObject


import random
AllSims = { }
###############################################################################
def index(request):

    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('fo:home')
    else:
        return redirect('fo:login')
    
def loadAllClassSims():
    group = Sim.objects.all().values_list('sim_identifier', flat=True)
    data = numpy.asarray(group)
    print(group)
    if (data.all()!=None):
        for e in range(len(data)):
            sim = Sim.objects.get(pk=data[e])
            sim_id = sim.sim_identifier
            print('\n  SIM IDENTIFIER : ',sim_id,'\n')
            AllSims[sim_id] = SimObject()
    print(AllSims)

###############################################################################
def testappHome(request):
    if request.method == 'POST':
        form = SimForm(request.POST)
        if form.is_valid():
            sim_name = form.cleaned_data.get('sim_name')
            sim = Sim.objects.create(sim_name = sim_name)
            display_init = DisplayBufferItem.objects.create(buffer_item = sim_name + " initialized")
            sim.display_buffer.add(display_init)
            sim.save()
    form = SimForm()
    sims = Sim.objects.all()
    return render(request, 'testapp/testapphome.html', {"sims": sims, "form": form})

############################################################################
def newSim(request):

    if request.method == 'POST':
        form = SimForm(request.POST)

        if form.is_valid():
            #loadAllClassSims()
            sim_name = form.cleaned_data.get('sim_name')
            
            

            unique_number = random.randint(10000,50000)
            unique_check = False
            while (unique_check == False):
                if unique_number not in AllSims:
                    unique_check = True
                    AllSims[unique_number] = SimObject(simName=sim_name)

            sim = Sim.objects.create(sim_name = sim_name)
            sim.sim_identifier = unique_number
            print('UNIWUE: ', sim.sim_identifier)
            print(AllSims)
            AllSims[unique_number].startSim()
            print()

            init_display = DisplayBufferItem.objects.create(buffer_item = sim_name + ' initialized')
            sim.display_buffer.add(init_display)

            sim.save()

            return redirect('../home')
    sims = Sim.objects.all()
    form = SimForm()
    
    return render(request, 'testapp/newSim.html', {"form": form, "sims": sims})

#########################################################################################################
def newMission(request):
    
    ###############################################3
    if request.method == 'POST':
        form2 = MissionCreationForm(request.POST)

        if form2.is_valid():
            
            mission_name = form2.cleaned_data.get('mission_name')

            mission = Mission.objects.create(mission_name = mission_name)
            TestConductor.objects.get(pk = 1).missions.add(mission)
            
            return redirect('../home')
                
    form2 = MissionCreationForm()
    return render(request, 'tc/newMission.html', {"form2":form2,})

###############################################################################
def testappSim(request, simkey):
    simobj = get_object_or_404(Sim, pk=simkey)
    return render(request, 'testapp/testappsim.html', {'sim': simobj, 'simkey': simkey})

###############################################################################
def submit(request, simkey):
    if request.method == 'GET':
           command = request.GET.get('cmd')  # String
           display_command = DisplayBufferItem.objects.create(buffer_item = command + " recieved")
           sim = Sim.objects.get(pk = simkey)
           sim.display_buffer.add(display_command)
           sim.save()
           return HttpResponse(command) # Sending an success response
    else:
           return HttpResponse("Request method is not a GET")

###############################################################################
def fetchdata(request, simkey):
    if request.method == 'GET':
        simobj = Sim.objects.get(pk = simkey)
        display_buffer = simobj.display_buffer.all()
        display_list = []
        for item in display_buffer:
            display_list.append(item.buffer_item)
        return HttpResponse(json.dumps(display_list)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")



