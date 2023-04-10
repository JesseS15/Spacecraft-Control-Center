from django.contrib import messages
import numpy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import JoinClassForm
from .models import FlightOperator
from tc.models import Class
from simapp.models import Sim

from django.http import JsonResponse
from django.template.loader import render_to_string
import json
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
@login_required(login_url='/login/')
def sim(request, simkey):
    
    sim = get_object_or_404(Sim, pk = simkey)
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    subsystem = _get_fo_subsystem(sim, flightOperator)
    if subsystem == 'DIRECTOR':
        return redirect('fo:acs', simkey)
    elif subsystem == 'Comms':
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
        # Create command object for db
        command = request.GET.get('cmd')  # String

        # Determine Flight Operator's Subsystem
        sim = Sim.objects.get(pk = simkey)
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Get simcraft thread
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
        
        # Pass command to simcraft thread subsystem and add input console response
        if subsystem == 'DIRECTOR':
            pass
        elif subsystem == 'Comms':
            pass
        elif subsystem == 'ACS':
            data = simThread.subsystems['ACS'].command(command)
        elif subsystem == 'EPS':
            pass
        elif subsystem == 'TCS':
            pass

        return HttpResponse(command + " command recieved") # Sending an success response
        return HttpResponse(json.dumps(data)) # Sending an success response

        return HttpResponse(command + " command recieved") # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")

###############################################################################
def fetchdata(request, simkey):
    if request.method == 'GET':
        # Get sim and flight operator subsystem
        sim = Sim.objects.get(pk = simkey)
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Define data strucutre to be returned
        data = {}
        data['output'] = []
        data['input'] = []
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
        
        if simThread == None:
            data['output'].append("Spacecraft Simulation for " + sim.sim_name + " has terminated execution")
            data['input'].append("Spacecraft Simulation for " + sim.sim_name + " has terminated execution")
        #if subsystem == 'DIRECTOR':
        #    for item in sim.director_command_buffer.all():
        #        data['input'].append(item.buffer_item)
        #elif subsystem == 'Comms':
        #    for item in sim.COMMS_command_buffer.all():
        #        data['input'].append(item.buffer_item)
        elif subsystem == 'ACS':
            data['input'] = simThread.subsystems['ACS'].commandLog
        #elif subsystem == 'EPS':
        #    for item in sim.EPS_command_buffer.all():
        #        data['input'].append(item.buffer_item)
        #elif subsystem == 'TCS':
        #    for item in sim.TCS_command_buffer.all():
        #        data['input'].append(item.buffer_item)
        
        return HttpResponse(json.dumps(data)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")

#######################################################################
def fetchcommands(request, simkey):
    if request.method == 'GET':
        # Get sim and flight operator subsystem
        sim = Sim.objects.get(pk = simkey)
        flightOperator = get_object_or_404(FlightOperator, user = request.user)
        subsystem = _get_fo_subsystem(sim, flightOperator)
        
        # Define data strucutre to be returned
        data = {
            'commands' : [],
        }
        
        # Get simcraft thread
        simThread = None
        thread_id = sim.sim_identifier
        for thread in threading.enumerate():
            if thread.ident == thread_id:
                simThread = thread
        
        if simThread == None:
            data['commands'].append("Spacecraft Simulation for " + sim.sim_name + " has terminated execution")
        #if subsystem == 'DIRECTOR':
        #    for item in sim.director_command_buffer.all():
        #        data['input'].append(item.buffer_item)
        #elif subsystem == 'Comms':
        #    for item in sim.COMMS_command_buffer.all():
        #        data['input'].append(item.buffer_item)
        elif subsystem == 'ACS':
            data['commands'] = simThread.subsystems['ACS'].commands
        #elif subsystem == 'EPS':
        #    for item in sim.EPS_command_buffer.all():
        #        data['input'].append(item.buffer_item)
        #elif subsystem == 'TCS':
        #    for item in sim.TCS_command_buffer.all():
        #        data['input'].append(item.buffer_item)
        
        return HttpResponse(json.dumps(data)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")

#######################################################################
@login_required(login_url='/login/')
def foClass(request, class_name):
    getFO = FlightOperator.objects.get(user = request.user)
    print(getFO)
    getclass = Class.objects.get(class_name=class_name)
    getFOsims = getFO.sim_list.all()
    print(getFOsims)
    getclasssims = getclass.sims.all()
    print(getclasssims)
    sims = []
    for sim in getFOsims:
        print(sim)
        if sim in getclasssims:
            print(sim)
            sims.append(sim)

    return render(request, 'fo/foClass.html', {'sims':sims, 'class_name':class_name})

def _get_fo_subsystem(simobj, flightOperator):
    subsystem = 'UNKNOWN'
    if simobj.flight_director.all():
        if flightOperator == simobj.flight_director.all()[0]:
            subsystem = 'DIRECTOR'
    if simobj.COMMS_fo.all():
        if flightOperator == simobj.COMMS_fo.all()[0]:
            subsystem = 'Comms'
    if simobj.ACS_fo.all():
        if flightOperator == simobj.ACS_fo.all()[0]:
            subsystem = 'ACS'
    if simobj.EPS_fo.all():
        if flightOperator == simobj.EPS_fo.all()[0]:
            subsystem = 'EPS'
    if simobj.TCS_fo.all():   
        if flightOperator == simobj.TCS_fo.all()[0]:
            subsystem = 'TCS'
    return subsystem