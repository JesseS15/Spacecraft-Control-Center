# STaTE
# File: tc/views.py
# Purpose: This file defines what html file and data to return when an http request is made to the tc Django app

from django.db import models
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ClassForm, ClassEditForm, SimEditForm, MissionEditForm
from .models import TestConductor, Class
from simapp.models import Sim, Mission

import json
import numpy
import random
import string
import threading
import time

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
    
    # Create new TestConductor object if none exists for current staff user
    if not TestConductor.objects.filter(user = request.user).exists():
        TestConductor.objects.create(user = request.user).save()
    tcobj = TestConductor.objects.get(user = request.user)

    if request.method == 'POST':
        form = ClassForm(request.POST)
        classes1 = Class.objects.all()
        classes = numpy.asarray(classes1)
        var = False
        if(form.is_valid()):
            class_namef = form.cleaned_data.get('class_name')
            nospacename = class_namef.replace(" ", "")
            test = form.cleaned_data.get('test')
            missions = numpy.asarray(request.POST.getlist('missions'))
            classesstr = str(classes)

            ifequal = 0
            for classi in classes:
                classstr = str(classi)
                if(str(classstr) == nospacename):
                    ifequal = ifequal+1
            
            if(len(classes)<=0):
                form.save()
                classget = Class.objects.get(class_name = class_namef)
                nospacename = class_namef.replace(" ", "")
                rcg = ''.join(random.choices(string.ascii_uppercase +string.digits, k=8))
                classget.class_name = nospacename
                classget.code = rcg
                classget.tc.add(tcobj)
                if(len(numpy.asarray(request.POST.getlist('missions'))))>=1:
                    for x in missions:
                        classget.missions.add(x)
                classget.save()
                tcobj = TestConductor.objects.get(user = request.user)
                tcobj.classes.add(classget)
                tcobj.save()
                return redirect('tc:home')
            elif(len(classes)>0 and ifequal==0 and test==True):
                form.save()
                classget = Class.objects.get(class_name = class_namef)
                nospacename = class_namef.replace(" ", "")
                rcg = ''.join(random.choices(string.ascii_uppercase +string.digits, k=8))
                classget.class_name = nospacename
                classget.code = rcg
                classget.tc.add(tcobj)
                if(len(numpy.asarray(request.POST.getlist('missions'))))>=1:
                    for x in missions:
                        classget.missions.add(x)
                classget.save()
                classget.save()
                tcobj = TestConductor.objects.get(user = request.user)
                tcobj.classes.add(classget)
                tcobj.save()
                return redirect('tc:home')
            elif(len(classes)>0 and ifequal>=1 and test ==True):
               messages.info(request, 'Class Already Exists. Add Class UNSUCCESSFUL')
               return redirect('tc:home')
    else:
        form = ClassForm()

    if request.method == 'POST':
        form2 = ClassEditForm(request.POST)
        classes1 = Class.objects.all()
        classes = numpy.asarray(classes1)
        if(form2.is_valid()):
            class_namef = form.cleaned_data.get('class_name')
            test = form2.cleaned_data.get('test')
            delete = form2.cleaned_data.get('delete')
            randomizecode = form2.cleaned_data.get('randomizecode')

            ifequal = 0
            for classi in classes:
                classstr = str(classi)
                if(str(classstr) == class_namef):
                    ifequal = ifequal+1
            
            if(len(classes)>0 and ifequal>=1):
                for classi in classes:
                    if(str(classi) == class_namef):
                        classget = Class.objects.get(class_name = class_namef)
                        if(delete==False):
                            if(randomizecode == False):
                                if(len(form2.cleaned_data.get('code'))>0):
                                    classget.code = form2.cleaned_data.get('code')
                                    if(len(numpy.asarray(request.POST.getlist('missions'))))>=1:
                                        classget.missions.add(numpy.asarray(request.POST.getlist('missions')))
                                    classget.save()
                                    return redirect('tc:home')
                                else:
                                    if(len(numpy.asarray(request.POST.getlist('missions'))))>=1:
                                        for x in missions:
                                            classget.missions.add(x)
                                    classget.save()
                                    return redirect('tc:home')
                            elif(randomizecode == True and (len(form2.cleaned_data.get('code'))>=1)):
                                 messages.info(request, 'Cannot enter code and randomize code. Please make one choice. Edit Unsuccessful.')  
                            else:
                                rcg = ''.join(random.choices(string.ascii_uppercase +string.digits, k=8))
                                classget.code = rcg
                                if(len(numpy.asarray(request.POST.getlist('missions'))))>=1:
                                    for x in missions:
                                        classget.missions.add(x)
                                classget.save()
                                return redirect('tc:home')
                        else:
                            classget.delete()
                            
            return redirect('tc:home')
    else:
        form2 = ClassEditForm()

    return render(request, 'tc/tcHome.html', {"classes":classes, 'form': form, 'form2': form2, 'tcobj':tcobj})
  
###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def classHome(request, class_name):

    group = Class.objects.all().filter(class_name = class_name).values_list('sims', flat=True)
    data = numpy.asarray(group)
    if (data.all()!=None):
        sims = ['']*(len(data))
        for e in range(len(data)):
            sims[e] = Sim.objects.get(pk=data[e])
    else:
        sims=[]
    #############################################################################
    group2 = Class.objects.all().filter(class_name = class_name).values_list('missions', flat=True)
    data2 = numpy.asarray(group2)
    if (data2.all()!=None):
        missions = ['']*(len(data2))
        for e in range(len(data2)):
            missions[e] = Mission.objects.get(pk=data2[e])
    else:
        missions=[] 
    
    ######################sim edit page#########################################
    if request.method == 'POST' and request.POST.get("form_type") == 'formOne':
        form3 = SimEditForm(request.POST)
        if(form3.is_valid()):
            sim_namef = request.POST.get('sim_name')
            delete = form3.cleaned_data.get('delete')
            simget = Class.objects.get(class_name = class_name).sims.get(sim_name=sim_namef)
            if(delete==False):
                simget.save()
            else:
                simThread = None
                thread_id = simget.sim_identifier
                for thread in threading.enumerate():
                    if thread.ident == thread_id:
                        simThread = thread
                if simThread != None:
                    simThread.stop()
                    simThread.join()
                simget.delete()
        return redirect('../home/'+class_name)
    else:
        form3 = SimEditForm()

    ###############################################################################
    if request.method == 'POST' and request.POST.get("form_type") == 'formTwo':
        form4 = MissionEditForm(request.POST)
        if(form4.is_valid()):
            mission_namef = request.POST.get('missionname')
            delete = form4.cleaned_data.get('delete')
            missionget = Mission.objects.get(mission_name = mission_namef)
            if(delete==False):
                missionget.save()
            else:
                missionget.delete()
        return redirect('../home/'+class_name)
    else:
        form4 = MissionEditForm()
########################################################
    # 3/5/23 Removed "missions":missions
    return render(request, 'tc/classHome.html', {"class_name": class_name, "sims":sims, "missions":missions, "form3":form3, "form4":form4})

###############################################################################
def getGroups(request):
    
    group = list(request.user.groups.values_list('name', flat = True))
    data = numpy.asarray(group)
    return render(request, 'tc: home.html', {"data":data})

def downloadSimReport(request):
    if request.method == 'GET':
        simkey= request.GET.get('simkey')
        sim = get_object_or_404(Sim, pk = simkey)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
                
        data = {}
        data['sim_name'] = sim.sim_name
        data['report'] = 'Report for Simulation: ' + sim.sim_name + '\n\n'
        
        if simThread != None:
            
            # Add ACS FO and Console Log
            data['report'] += 'Report for ACS subsytem: \n'
            data['report'] += '\tACS Flight Operator: ' + str(sim.ACS_fo) + '\n'
            data['report'] += '\tACS Console Log:\n'
            for item in simThread.subsystems['ACS'].consoleLog:
                data['report'] += '\t\t' + item + '\n'
            data['report'] += '\n'
            
            # Add EPS FO and Console Log
            data['report'] += 'Report for EPS subsytem: \n'
            data['report'] += '\tEPS Flight Operator: ' + str(sim.EPS_fo) + '\n'
            data['report'] += '\tEPS Console Log:\n'
            for item in simThread.subsystems['EPS'].consoleLog:
                data['report'] += '\t\t' + item + '\n'
            data['report'] += '\n'
            
            # Add TCS FO and Console Log
            data['report'] += 'Report for TCS subsytem: \n'
            data['report'] += '\tTCS Flight Operator: ' + str(sim.TCS_fo) + '\n'
            data['report'] += '\tTCS Console Log:\n'
            for item in simThread.subsystems['TCS'].consoleLog:
                data['report'] += '\t\t' + item + '\n'
            data['report'] += '\n'
            
            # Add COMMs FO and Console Log
            data['report'] += 'Report for Comms subsytem: \n'
            data['report'] += '\tComms Flight Operator: ' + str(sim.COMMS_fo) + '\n'
            data['report'] += '\tComms Console Log:\n'
            for item in simThread.subsystems['COMMS'].consoleLog:
                data['report'] += '\t\t' + item + '\n'
            data['report'] += '\n'
            
            # Add Payload FO and Console Log
            data['report'] += 'Report for Payload subsytem: \n'
            data['report'] += '\tPayload Flight Operator: ' + str(sim.flight_director) + '\n'
            data['report'] += '\tPayload Console Log:\n'
            for item in simThread.subsystems['Payload'].consoleLog:
                data['report'] += '\t\t' + item + '\n'
            data['report'] += '\n'

        return HttpResponse(json.dumps(data)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")

###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def tcSim(request, simkey):
    return redirect('tc:acs', simkey)
    
###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def acs(request, simkey):

    simobj = get_object_or_404(Sim, pk = simkey)
    return render(request, 'tc/acs.html', {'sim': simobj, 'simkey': simkey})

###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def eps(request, simkey):

    simobj = get_object_or_404(Sim, pk = simkey)
    return render(request, 'tc/eps.html', {'sim': simobj, 'simkey': simkey})

###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def tcs(request, simkey):
    
    simobj = get_object_or_404(Sim, pk = simkey)
    return render(request, 'tc/tcs.html', {'sim': simobj, 'simkey': simkey})

###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def payload(request, simkey):

    simobj = get_object_or_404(Sim, pk = simkey)
    return render(request, 'tc/payload.html', {'sim': simobj, 'simkey': simkey})

###############################################################################
@login_required(login_url='/login/')
@staff_member_required
def comms(request, simkey):

    simobj = get_object_or_404(Sim, pk = simkey)
    return render(request, 'tc/comms.html', {'sim': simobj, 'simkey': simkey})

###############################################################################
def acsFetchdata(request, simkey):
    if request.method == 'GET':
        sim = get_object_or_404(Sim, pk = simkey)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
                
        data = {}
         
        if simThread != None:
            # Define data to be returned
            
            data['roll'] = simThread.subsystems['ACS'].orientation['roll']
            data['pitch'] = simThread.subsystems['ACS'].orientation['pitch']
            data['yaw'] = simThread.subsystems['ACS'].orientation['yaw']
            data['longitude'] = simThread.subsystems['ACS'].currentLongitude
            
            data['cmg_roll'] = simThread.subsystems['ACS'].rollActive
            data['cmg_pitch'] = simThread.subsystems['ACS'].pitchActive
            data['cmg_yaw'] = simThread.subsystems['ACS'].yawActive
            
            data['cmg_status'] = simThread.subsystems['ACS'].cmgStatus
            data['orientation_relay'] = simThread.subsystems['ACS'].orientationRelay
            
            data['telemetry_Transferring'] = simThread.subsystems['ACS'].telemetryTransferring
            data['telemetry_Transferred'] = simThread.subsystems['ACS'].telemetryTransferComplete
        
        return HttpResponse(json.dumps(data)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")
    
###############################################################################
def epsFetchdata(request, simkey):
    if request.method == 'GET':
        sim = get_object_or_404(Sim, pk = simkey)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
                
        data = {}
         
        if simThread != None:
            # Define data to be returned
            
            data['acs_power'] = simThread.subsystems['EPS'].distribution['ACS']
            data['eps_power'] = simThread.subsystems['EPS'].distribution['EPS']
            data['tcs_power'] = simThread.subsystems['EPS'].distribution['TCS']
            data['comms_power'] = simThread.subsystems['EPS'].distribution['COMMS']
            data['payload_power'] = simThread.subsystems['EPS'].distribution['Payload']
            
            data['articulation'] = simThread.subsystems['EPS'].solarPanelAngle
            data['total_power'] = simThread.subsystems['EPS'].totalPower
            
            data['telemetry_Transferring'] = simThread.subsystems['EPS'].telemetryTransferring
            data['telemetry_Transferred'] = simThread.subsystems['EPS'].telemetryTransferComplete
        
        return HttpResponse(json.dumps(data)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")
    
###############################################################################
def tcsFetchdata(request, simkey):
    if request.method == 'GET':
        sim = get_object_or_404(Sim, pk = simkey)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
                
        data = {}
         
        if simThread != None:
            # Define data to be returned
            
            data['CMG-Temp'] = simThread.subsystems['TCS'].ACSThermal["CMG"]
            data['Alignment-Temp'] = simThread.subsystems['TCS'].ACSThermal["Alignment System"]
            
            data['Distribution-Temp'] = simThread.subsystems['TCS'].EPSThermal["Power Distribution"]
            data['Battery-Temp'] = simThread.subsystems['TCS'].EPSThermal["Battery"]
            data['Articulation-Temp'] = simThread.subsystems['TCS'].EPSThermal["Articulation System"]
            
            data['Computer-Temp'] = simThread.subsystems['TCS'].COMMSThermal["On-board Computer"]
            data['Processor-Temp'] = simThread.subsystems['TCS'].COMMSThermal["Signal Processor"]
            
            data['Optical-Temp'] = simThread.subsystems['TCS'].PayloadThermal["Optical Electronics"]
            data['Gimbal-Temp'] = simThread.subsystems['TCS'].PayloadThermal["Gimbal System"]
            data['Imager-Temp'] = simThread.subsystems['TCS'].PayloadThermal["Imager"]
            
            data['telemetry_Transferring'] = simThread.subsystems['TCS'].telemetryTransferring
            data['telemetry_Transferred'] = simThread.subsystems['TCS'].telemetryTransferComplete
        
        return HttpResponse(json.dumps(data)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")

###############################################################################
def commsFetchdata(request, simkey):
    if request.method == 'GET':
        sim = get_object_or_404(Sim, pk = simkey)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
                
        data = {}
         
        if simThread != None:
            # Define data to be returned
            
            data['Telemetry-ACS'] = simThread.subsystems['COMMS'].allTelemetryData['ACS']
            data['Telemetry-EPS'] = simThread.subsystems['COMMS'].allTelemetryData['EPS']
            data['Telemetry-TCS'] = simThread.subsystems['COMMS'].allTelemetryData['TCS']
            data['Telemetry-Payload'] = simThread.subsystems['COMMS'].allTelemetryData['Payload']
            
            data['On-Board-Computer'] = simThread.subsystems['COMMS'].checks['On-board Computer']
            data['Antenna-Status'] = simThread.subsystems['COMMS'].checks['Antenna Status']
            
            data['Bandwidth'] = simThread.subsystems['COMMS'].frequency
            data['Gain'] = simThread.subsystems['COMMS'].currentGain
            
            data['Target'] = simThread.telemetry['ACS']
            data['Image'] = simThread.telemetry['Payload']
            data['Status'] = simThread.subsystems['COMMS'].allTelemetryDataGood
        
        return HttpResponse(json.dumps(data)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")
    
###############################################################################
def payloadFetchdata(request, simkey):
    if request.method == 'GET':
        sim = get_object_or_404(Sim, pk = simkey)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
                
        data = {}
         
        if simThread != None:
            # Define data to be returned

            data['Connection'] = simThread.subsystems['Payload'].statusGood
            
            data['In-Range'] = simThread.subsystems['Payload'].slewImageFlag
            data['Target-Acquired'] = simThread.subsystems['Payload'].acquireTargetFlag
            data['Image-Received'] = simThread.subsystems['Payload'].captureImageFlag

            data['Gimbal-Status'] = simThread.subsystems['Payload'].gimbalStatus
            data['Imager-Status'] = simThread.subsystems['Payload'].imagerStatus

            data['Optical-Electronics'] = simThread.subsystems['Payload'].checks['Optical Electronics']
            data['Bus-Connection'] = simThread.subsystems['Payload'].checks['Bus Connection']
            data['Gimbal-Connection'] = simThread.subsystems['Payload'].checks['Gimble Connection']
        
            data['telemetry_Transferring'] = simThread.subsystems['Payload'].telemetryTransferring
            data['telemetry_Transferred'] = simThread.subsystems['Payload'].telemetryTransferComplete
        
        return HttpResponse(json.dumps(data)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")