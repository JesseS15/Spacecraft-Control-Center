# STaTE
# File: simapp/views.py
# Purpose: This file defines what html file and data to return when an http request is made to the simapp Django app

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Sim, Mission
from fo.models import FlightOperator
from tc.forms import *
from tc.models import *

from simulation.SimObject import SimObject

import numpy, random

############################################################################
def newSim(request, class_name):
    
    # Ensure selected class has at least one mission
    selected_class = Class.objects.get(class_name=class_name)
    if selected_class.missions.all().count() == 0:
        if TestConductor.objects.get(user = request.user).missions.all().count() == 0: # No missions in any class
            messages.info(request, 'You do not have any existing missions: create a new one')
        else: # No missions in selected class
            messages.info(request, 'You do not have any missions in this class: add an existing mission or create a new one')
        return redirect('../'+class_name+'/newMission')

    if request.method == 'POST':
        form = SimCreationForm(class_name, request.POST)

        if form.is_valid():
            sim_name = form.cleaned_data.get('sim_name')
            sim_exists = selected_class.sims.filter(sim_name=sim_name).exists()

            if not sim_exists:
                sim = Sim.objects.create(sim_name = sim_name, 
                                         mission_script = form.cleaned_data.get('mission_script'), 
                                         flight_director= form.cleaned_data.get('flight_director'),
                                         COMMS_fo= form.cleaned_data.get('COMMS_fo'),
                                         ACS_fo=form.cleaned_data.get('ACS_fo'), 
                                         TCS_fo=form.cleaned_data.get('TCS_fo'), 
                                         EPS_fo=form.cleaned_data.get('EPS_fo'))
                mission = sim.mission_script
                final_values = {}
                final_values["roll"] = mission.final_roll
                final_values["pitch"] = mission.final_pitch
                final_values["yaw"] = mission.final_yaw
                
                sim.ACS_fo.sim_list.add(sim)
                sim.fo_list.add(sim.ACS_fo)
                
                sim.EPS_fo.sim_list.add(sim)
                sim.fo_list.add(sim.EPS_fo)
        
                sim.TCS_fo.sim_list.add(sim)
                sim.fo_list.add(sim.TCS_fo)
                
                sim.COMMS_fo.sim_list.add(sim)
                sim.fo_list.add(sim.COMMS_fo)
                
                sim.flight_director.sim_list.add(sim)
                sim.fo_list.add(sim.flight_director)

                # Create and start new sim thread
                simThread = SimObject(final_values, pk=sim.pk)
                simThread.start()
                
                sim.sim_identifier = simThread.ident
                sim.save()
                
                selected_class.sims.add(sim)
                
                
                return redirect('tc:classHome', class_name)
            else:
                messages.info(request, 'Sim with the same name already exists in this class. Please choose a different name.')
        else:
            messages.info(request, 'Invalid form data.')
            
    else:
        form = SimCreationForm(class_name)
        
    sims = selected_class.sims
    return render(request, 'tc/newSim.html', {"form": form, "class_name": class_name, "sims": sims})

#########################################################################################################
@login_required(login_url='/login/')
def newMission(request,class_name):

    if request.method == 'POST':
        form2 = MissionCreationForm(request.POST)

        if form2.is_valid():
                classselect = Class.objects.all().get(class_name = class_name)
                misobjects = Mission.objects.all()
                missions = numpy.asarray(misobjects)
                mission_name = form2.cleaned_data.get('mission_name')
                missionnamenospace = mission_name.replace(" ", "")
                final_roll = form2.cleaned_data.get('final_roll')
                final_pitch = form2.cleaned_data.get('final_pitch')
                final_yaw = form2.cleaned_data.get('final_yaw')
                ifequal = 0
                for missioncheck in missions:
                    missionstr = str(missioncheck)
                    if(str(missionstr) == missionnamenospace):
                        ifequal = ifequal+1
                
                if(len(missions)<=0):
                    nospacename = mission_name.replace(" ", "")
                    mission = Mission.objects.create(mission_name = nospacename, verbose_name = mission_name)
                    classselect.missions.add(mission)
                    ifequal = 0
                    # Create new Sim Database object
                if(len(missions)>0 and ifequal>0):
                    messages.info(request, 'Mission Already Exists. Add Mission UNSUCCESSFUL')
                    return redirect('../'+class_name+'/newMission')
                if(len(missions)>0 and ifequal<=0):
                    nospacename = mission_name.replace(" ", "")
                    mission = Mission.objects.create(mission_name = nospacename, verbose_name = mission_name)
                    classselect.missions.add(mission)
                    ifequal = 0

                mission.final_roll = final_roll
                mission.final_pitch = final_pitch
                mission.final_yaw = final_yaw
                mission.save()
                TestConductor.objects.get(user = request.user).missions.add(mission)
                
                return redirect('../'+class_name)
    form2 = MissionCreationForm()
    return render(request, 'tc/newMission.html', {"form2":form2, "class_name": class_name})
