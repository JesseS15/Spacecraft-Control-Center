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

import simapp.funcs as RegularFunctions

All_Sims_Dict = { }

############################################################################
@login_required(login_url='/login/')
def newSim(request,class_name):

    missions = TestConductor.objects.get().missions.all()
    marray = numpy.asarray(missions)
    print('   MISSIONGS ',marray)
    if (len(marray)==0):
        return redirect('../'+class_name+'/newMission')



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
            mission = form.cleaned_data.get('mission_script')
            flight_director = form.cleaned_data.get('flight_director')
            COMMS_fo = form.cleaned_data.get('COMMS_fo')
            ACS_fo = form.cleaned_data.get('ACS_fo')
            EPS_fo = form.cleaned_data.get('EPS_fo')
            TCS_fo = form.cleaned_data.get('TCS_fo')

            RegularFunctions.repopulateAllSimsDict(All_Sims_Dict)
            unique_number = RegularFunctions.getUniqueValue(All_Sims_Dict)
            All_Sims_Dict[unique_number] = SimObject(simName=sim_name)
            

            print('Dictionary: ',All_Sims_Dict)

            sim = Sim.objects.create(sim_name = sim_name, mission_script = mission)
            sim.sim_identifier = unique_number
            print('SIM ID views: ',sim.sim_identifier)

            sim.flight_director.set(flight_director)
            #sim.mission_script = mission
            sim.COMMS_fo.set(COMMS_fo)
            sim.ACS_fo.set(ACS_fo)
            sim.TCS_fo.set(EPS_fo)
            sim.EPS_fo.set(TCS_fo)

            m = sim.mission_script
            final_values = {}
            final_values["roll"] = m.final_roll
            final_values["pitch"] = m.final_pitch
            final_values["yaw"] = m.final_yaw
            final_values["longitude"] = m.final_longitude
            All_Sims_Dict[sim.sim_identifier].finalDict = final_values

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
            final_roll = form2.cleaned_data.get('final_roll')
            final_pitch = form2.cleaned_data.get('final_pitch')
            final_yaw = form2.cleaned_data.get('final_yaw')
            final_longitude = form2.cleaned_data.get('final_longitude')
            start_longitude = form2.cleaned_data.get('start_longitude')

            mission = Mission.objects.create(mission_name = mission_name)

            mission.final_roll = final_roll
            mission.final_pitch = final_pitch
            mission.final_yaw = final_yaw
            mission.final_longitude = final_longitude
            mission.start_longitude = start_longitude

            TestConductor.objects.get().missions.add(mission)
            
            return redirect('../'+class_name)
                
    form2 = MissionCreationForm()
    return render(request, 'tc/newMission.html', {"form2":form2, "class_name": class_name})

#########################################################################################################
