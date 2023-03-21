from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
# Importing models from simaapp/views.py

from .models import Sim, Mission
from tc.forms import *
from tc.models import *
from tc.models import TestConductor, Class
import numpy
from django.contrib.auth.decorators import login_required

############################################################################
@login_required(login_url='/login/')
def newSim(request,class_name):
    print("hi"+class_name)
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
 
    this = Class.objects.all().filter(class_name = class_name).values_list('flight_operators', flat = True)
    flight = numpy.asarray(this)
    if (flight.all()!=None):
        fos = ['']*(len(flight))
        for m in range(len(flight)):
            print(FlightOperator.objects.get(pk=flight[m]))
            fos[m] = FlightOperator.objects.get(pk=flight[m])
        print(fos)
    else:
        fos=[]
    
    ######################################
    #form = SimCreationForm()
    if request.method == 'POST':
        form = SimCreationForm(class_name,request.POST)

        if form.is_valid():
            sim_list = form.cleaned_data.get('sim_list')
            sim_name = form.cleaned_data.get('sim_name')
            #sys_list = form.cleaned_data.get('sys_list')
            fd = form.cleaned_data.get('flight_director__user__username')
            COMMS_fo = form.cleaned_data.get('COMMS_fo')
            sim = Sim.objects.create(sim_name = sim_name)
            Class.objects.get(class_name = class_name).sims.add(sim)
            #for x in sys_list:
            #    sim.sys_list.add(x)
                #sys_list.sim_list.add(sim)
                #class_belong.sim_list.add(sim)
            #form.save_m2m()
            ##gohere
            print(sim)
            if fd.exists():
                print("caryyyyy")
                
                #fd.sim_list.add(sim)
                #for flight_operator in flight_director:
                    # Send notification
            """send_mail(
                'STaTE Simulation Added to Your Account',
                'A new simulation, ' + sim.sim_name + ', has been added to your STaTE account.',
                None,
                [flight_operator.user.email],
                fail_silently=False,
            )"""
            return redirect('../'+class_name)
            
    form = SimCreationForm(class_name)
    
    return render(request, 'tc/newSim.html', {"form": form, "class_name": class_name, "sims": sims})

#########################################################################################################
@login_required(login_url='/login/')
def newMission(request,class_name):
    print("hi"+class_name)
    
    ###############################################3
    if request.method == 'POST':
        form2 = MissionCreationForm(request.POST)

        if form2.is_valid():
            
            mission_name = form2.cleaned_data.get('mission_name')

            mission = Mission.objects.create(mission_name = mission_name)
            TestConductor.objects.get().missions.add(mission)
            
            return redirect('../'+class_name)
                
    form2 = MissionCreationForm()
    return render(request, 'tc/newMission.html', {"form2":form2, "class_name": class_name})