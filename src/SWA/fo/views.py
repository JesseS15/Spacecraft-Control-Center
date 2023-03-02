from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import JoinClassForm
from .models import FlightOperator
from tc.models import Class
from simapp.models import Sim, Subsystem

from django.http import JsonResponse
from django.template.loader import render_to_string
import json

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
    return render(request, 'fo/foHome.html', {'flightOperator':flightOperator})

###############################################################################
@login_required(login_url='/login/')
def foSim(request, simkey):

    simobj = get_object_or_404(Sim, pk=simkey)
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    if simobj in flightOperator.sim_list.all():
        return render(request, 'fo/foSim.html', {'sim': simobj, 'simkey': simkey})
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
            return redirect('fo:home')
            
        else:
            messages.info(request, f'Class does not exist')

    form = JoinClassForm()
    return render(request, 'fo/joinClass.html', {'form':form})

###############################################################################
def submit(request, simkey):
    if request.method == 'GET':
           command = request.GET.get('cmd')  # String
           sim = Sim.objects.get(pk = simkey)
           #sim.command = command
           #sim.save()
           #print("py " + command)
           return HttpResponse("todo") # Sending an success response
    else:
           return HttpResponse("Request method is not a GET")

###############################################################################
def fetchdata(request, simkey):
    if request.method == 'GET':
        simobj = Sim.objects.get(pk = simkey)
        return HttpResponse("todo") # Sending an success response
    else:
        return HttpResponse("Request method is not GET")