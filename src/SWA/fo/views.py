# STaTE
# File: fo/views.py
# Purpose: This file defines what html file and data to return when an http request is made to the fo Django app

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404

from .forms import JoinClassForm
from .models import FlightOperator
from simapp.models import Sim
from tc.models import Class

import json
import numpy
import threading

###############################################################################
def index(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('fo:home')
    else:
        return redirect('fo:login')

###############################################################################
@login_required(login_url='/login/')
def foHome(request):
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    classes = flightOperator.class_list.all()
    if request.method == 'POST':
        code = request.POST['code']
        class_names = [classobj.class_name for classobj in Class.objects.all()]
        codes = [classobj.code for classobj in Class.objects.all()]
        if code in codes:
            classobj = Class.objects.get(code = code)
            classobj.flight_operators.add(FlightOperator.objects.get(user = request.user))
            test = FlightOperator.objects.get(user = request.user)
            test.class_list.add(Class.objects.get(code = code))
            return redirect('fo:home')
        else:
            messages.info(request, f'Class does not exist')

    form = JoinClassForm()
    return render(request, 'fo/foHome.html', {'flightOperator':flightOperator, 'classes':classes, 'form':form})

###############################################################################
# Route flight operator to page for their assigned subsystem
@login_required(login_url='/login/')
def sim(request, simkey):
    sim = get_object_or_404(Sim, pk = simkey)
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    subsystem = _get_fo_subsystem(sim, flightOperator)
    if subsystem == 'Payload':
        return redirect('fo:payload', simkey)
    elif subsystem == 'COMMS':
        return redirect('fo:comms', simkey)
    elif subsystem == 'ACS':
        return redirect('fo:acs', simkey)
    elif subsystem == 'EPS':
        return redirect('fo:eps', simkey)
    elif subsystem == 'TCS':
        return redirect('fo:tcs', simkey)
    else:
        return redirect('fo:home')
    
###############################################################################
@login_required(login_url='/login/')
def acs(request, simkey):

    simobj = get_object_or_404(Sim, pk = simkey)
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    if simobj in flightOperator.sim_list.all():
        subsystem = _get_fo_subsystem(simobj, flightOperator)
        return render(request, 'fo/acs.html', {'sim': simobj, 'simkey': simkey, 'flightoperator': flightOperator, 'subsystem': subsystem})
    else:
        return redirect('fo:home')
###############################################################################
@login_required(login_url='/login/')
def eps(request, simkey):

    simobj = get_object_or_404(Sim, pk = simkey)
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    if simobj in flightOperator.sim_list.all():
        subsystem = _get_fo_subsystem(simobj, flightOperator)
        return render(request, 'fo/eps.html', {'sim': simobj, 'simkey': simkey, 'flightoperator': flightOperator, 'subsystem': subsystem})
    else:
        return redirect('fo:home')
###############################################################################
@login_required(login_url='/login/')
def tcs(request, simkey):

    simobj = get_object_or_404(Sim, pk = simkey)
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    if simobj in flightOperator.sim_list.all():
        subsystem = _get_fo_subsystem(simobj, flightOperator)
        return render(request, 'fo/tcs.html', {'sim': simobj, 'simkey': simkey, 'flightoperator': flightOperator, 'subsystem': subsystem})
    else:
        return redirect('fo:home')
###############################################################################
@login_required(login_url='/login/')
def payload(request, simkey):

    simobj = get_object_or_404(Sim, pk = simkey)
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    if simobj in flightOperator.sim_list.all():
        subsystem = _get_fo_subsystem(simobj, flightOperator)
        return render(request, 'fo/payload.html', {'sim': simobj, 'simkey': simkey, 'flightoperator': flightOperator, 'subsystem': subsystem})
    else:
        return redirect('fo:home')
###############################################################################
@login_required(login_url='/login/')
def comms(request, simkey):

    simobj = get_object_or_404(Sim, pk = simkey)
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    if simobj in flightOperator.sim_list.all():
        subsystem = _get_fo_subsystem(simobj, flightOperator)
        return render(request, 'fo/comms.html', {'sim': simobj, 'simkey': simkey, 'flightoperator': flightOperator, 'subsystem': subsystem})
    else:
        return redirect('fo:home')
    
###############################################################################
def joinClass(request):
    
    if request.method == 'POST':
        class_name = request.POST['class_name']
        class_names = [classobj.class_name for classobj in Class.objects.all()]
        if class_name in class_names:
            classobj = Class.objects.get(class_name = class_name)
            classobj.flight_operators.add(FlightOperator.objects.get(user = request.user))
            test = FlightOperator.objects.get(user = request.user)
            test.class_list.add(Class.objects.get(class_name = class_name))
            return redirect('fo:home')
        else:
            messages.info(request, f'Class does not exist')

    form = JoinClassForm()
    return render(request, 'fo/joinClass.html', {'form':form})

###############################################################################
def submit(request, simkey):
    if request.method == 'GET':
        command = request.GET.get('cmd')  # String

        # Determine Flight Operator's Subsystem
        sim = get_object_or_404(Sim, pk = simkey)
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
        
        # Pass command to simcraft thread subsystem and add input console response
        if simThread == None:
            response = ["Spacecraft Simulation for " + sim.sim_name + " has terminated execution"]
            sim.status = "INACTIVE"
            sim.save()
        elif subsystem != 'UNKNOWN':
            response = simThread.subsystems[subsystem].command(command)
        else:
            response = []

        return HttpResponse(json.dumps(response)) # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")
    
###############################################################################
def acsFetchdata(request, simkey):
    if request.method == 'GET':
        sim = get_object_or_404(Sim, pk = simkey)
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
                
        data = {}
                
        if simThread != None and subsystem != 'UNKNOWN':
            # Define data to be returned
            data['consoleLog'] = simThread.subsystems[subsystem].consoleLog
            
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
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
                
        data = {}
                
        if simThread != None and subsystem != 'UNKNOWN':
            # Define data to be returned
            data['consoleLog'] = simThread.subsystems[subsystem].consoleLog
            
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
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
            
        data = {}
        
        if simThread != None and subsystem != 'UNKNOWN':
            # Define data to be returned
            data['consoleLog'] = simThread.subsystems[subsystem].consoleLog
            
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
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
                
        data = {}
        
        if simThread != None and subsystem != 'UNKNOWN':
            # Define data to be returned
            data['consoleLog'] = simThread.subsystems[subsystem].consoleLog
            
            data['Telemetry-ACS'] = simThread.telemetry['ACS']
            data['Telemetry-EPS'] = simThread.telemetry['EPS']
            data['Telemetry-TCS'] = simThread.telemetry['TCS']
            data['Telemetry-Payload'] = simThread.telemetry['Payload']
            
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
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
               
        data = {}
        data['consoleLog'] = []
         
        if simThread != None and subsystem != 'UNKNOWN':
            # Define data to be returned
            data['consoleLog'] = simThread.subsystems[subsystem].consoleLog
            
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

#######################################################################
def fetchcommands(request, simkey):
    if request.method == 'GET':
        # Get sim and flight operator subsystem
        sim = get_object_or_404(Sim, pk = simkey)
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Define data strucutre to be returned
        data = {
            'commandOptions' : [],
            'previousCommands': [],
        }
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
        
        if simThread == None:
            data['commandOptions'].append("Spacecraft Simulation for " + sim.sim_name + " has terminated execution")
            data['previousCommands'].append("Spacecraft Simulation for " + sim.sim_name + " has terminated execution")
            sim.status = "INACTIVE"
            sim.save()
        elif subsystem != 'UNKNOWN':
            data['commandOptions'] = simThread.subsystems[subsystem].commands
            data['previousCommands'] = simThread.subsystems[subsystem].consoleLog

        return HttpResponse(json.dumps(data)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")

#######################################################################
@login_required(login_url='/login/')
def foClass(request, class_name):
    getFO = FlightOperator.objects.get(user = request.user)
    getclass = Class.objects.get(class_name=class_name)
    getFOsims = getFO.sim_list.all()
    getclasssims = getclass.sims.all()
    sims = []
    for sim in getFOsims:
        if sim in getclasssims:
            sims.append(sim)

    return render(request, 'fo/foClass.html', {'sims':sims, 'class_name':class_name})

#######################################################################
@login_required(login_url='/login/')
def imagedisplay(request):
    return render(request, 'fo/imagedisplay.html', {})

#######################################################################
@login_required(login_url='/login/')
def rickdisplay(request):
    return render(request, 'fo/rickroll.html', {})

#######################################################################
def _get_fo_subsystem(simobj, flightOperator):
    subsystem = 'UNKNOWN'
    if flightOperator == simobj.flight_director:
        subsystem = "Payload"
    if flightOperator == simobj.COMMS_fo:
        subsystem = "COMMS"
    if flightOperator == simobj.ACS_fo:
        subsystem = "ACS"
    if flightOperator == simobj.EPS_fo:
        subsystem = "EPS"
    if flightOperator == simobj.TCS_fo:
        subsystem = "TCS"
    return subsystem
