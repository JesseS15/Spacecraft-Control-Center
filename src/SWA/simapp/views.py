from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
# Importing models from simaapp/views.py

from .models import Sim, Mission
from tc.forms import *
from tc.models import *
from tc.models import TestConductor, Class
import numpy, random
from django.contrib.auth.decorators import login_required
from tc.forms import SimCreationForm
from fo.models import FlightOperator
from simulation.SimObject import SimObject

All_Sims_Dict = { }

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
        form = SimCreationForm(class_name, request.POST)
        
        if form.is_valid():
            #form.save()
            print(form.cleaned_data)
           # sim_list = form.cleaned_data.get('sim_list')y
            sim_name = form.cleaned_data.get('sim_name')
            #sys_list = form.cleaned_data.get('sys_list')
            flight_director = form.cleaned_data.get('flight_director')
            COMMS_fo = form.cleaned_data.get('COMMS_fo')
            ACS_fo = form.cleaned_data.get('ACS_fo')
            EPS_fo = form.cleaned_data.get('EPS_fo')
            TCS_fo = form.cleaned_data.get('TCS_fo')
            
            ### Setting the unique number identifier for the SimObject object and models sim_identifier ###
            unique_number = random.randint(10000,50000)
            unique_check = False
            while (unique_check == False):
                if unique_number not in All_Sims_Dict:
                    unique_check = True
                    All_Sims_Dict[unique_number] = SimObject(simName=sim_name)

            print(All_Sims_Dict)

            sim = Sim.objects.create(sim_name = sim_name)
            sim.sim_identifier = unique_number

            sim.flight_director.set(flight_director)
            sim.COMMS_fo.set(COMMS_fo)
            sim.ACS_fo.set(ACS_fo)
            sim.TCS_fo.set(EPS_fo)
            sim.EPS_fo.set(TCS_fo)

            Class.objects.get(class_name = class_name).sims.add(sim)
            flight_operators = FlightOperator.objects.all()
            if (flight_director != None):
                for x in flight_operators:
                    x.sim_list.add(sim)

            if (COMMS_fo != None):
                for x in flight_operators:
                    x.sim_list.add(sim)
            
            if (ACS_fo != None):
                for x in flight_operators:
                    x.sim_list.add(sim)
            
            if (TCS_fo != None):
                for x in flight_operators:
                    x.sim_list.add(sim)
            
            if (EPS_fo != None):
                for x in flight_operators:
                    x.sim_list.add(sim)
    
                   # Send notification
            """send_mail(
                'STaTE Simulation Added to Your Account',
                'A new simulation, ' + sim.sim_name + ', has been added to your STaTE account.',
                None,
                [flight_operator.user.email],
                fail_silently=False,
            )"""
            return redirect('../'+class_name)
    else:
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