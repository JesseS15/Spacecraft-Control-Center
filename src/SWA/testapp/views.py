from django.contrib import messages
import numpy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SimForm

from .models import Sim, DisplayBufferItem

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