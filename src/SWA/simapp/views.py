from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
# Importing models from simaapp/views.py

from django.contrib import messages
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
def newSim(request, class_name):

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
            classattr = Class.objects.get(class_name = class_name)
            sims = classattr.sims.all()
            # Get sim values from form
            #form.save()
            print(form.cleaned_data)
            # sim_list = form.cleaned_data.get('sim_list')y
            sim_name = form.cleaned_data.get('sim_name')
            nospacename = sim_name.replace(" ", "")
            #sys_list = form.cleaned_data.get('sys_list')
            mission = form.cleaned_data.get('mission_script')
            flight_director = form.cleaned_data.get('flight_director')
            COMMS_fo = form.cleaned_data.get('COMMS_fo')
            ACS_fo = form.cleaned_data.get('ACS_fo')
            EPS_fo = form.cleaned_data.get('EPS_fo')
            TCS_fo = form.cleaned_data.get('TCS_fo')

            # Create new Sim Database object
            count = 0
            if(len(sims)>0):
                for x in sims:
                    if(x == nospacename):
                        count = count + 1
                if(count>0):
                    sim = Sim.objects.create(sim_name = nospacename, mission_script = mission)
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

                    # Create and start new sim thread
                    simThread = SimObject(final_values, pk=sim.pk)
                    simThread.start()
                    RegularFunctions.repopulateAllSimsDict(All_Sims_Dict)
                    All_Sims_Dict[sim.sim_identifier] = simThread
                    All_Sims_Dict[sim.sim_identifier].check()

                    print('Dictionary: ',All_Sims_Dict)

                    Class.objects.get(class_name = class_name).sims.add(sim)
                    flight_operators = FlightOperator.objects.all()
                    print(type(flight_operators))
                    if (flight_director.exists()):
                        for x in flight_operators:
                            if(str(x) == str((flight_director[0]))):
                                x.sim_list.add(sim)

                    if (COMMS_fo.exists()):
                        for x in flight_operators:
                            if(str(x) == str((COMMS_fo[0]))):
                                x.sim_list.add(sim)
                
                    if (ACS_fo.exists()):
                        for x in flight_operators:
                            if(str(x) == str((ACS_fo[0]))):
                                x.sim_list.add(sim)
                    
                    if (TCS_fo.exists()):
                        for x in flight_operators:
                            if(str(x) == str((TCS_fo[0]))):
                                x.sim_list.add(sim)
                    
                    if (EPS_fo.exists()):
                        for x in flight_operators:
                            if(str(x) == str((EPS_fo[0]))):
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
                    messages.info(request, 'Sim Already Exists. Add Class UNSUCCESSFUL')
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

            mission = Mission.objects.create(mission_name = mission_name)

            mission.final_roll = final_roll
            mission.final_pitch = final_pitch
            mission.final_yaw = final_yaw

            TestConductor.objects.get().missions.add(mission)
            
            return redirect('../'+class_name)
                
    form2 = MissionCreationForm()
    return render(request, 'tc/newMission.html', {"form2":form2, "class_name": class_name})

#########################################################################################################
