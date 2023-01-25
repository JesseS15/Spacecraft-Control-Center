from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegisterForm, SubsystemForm, JoinClassForm
from .models import FlightOperator
from tc.models import Sim, Class

###############################################################################
def index(request):

    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('fo:home')
    else:
        return redirect('fo:login')

###############################################################################
def foHome(request):
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    return render(request, 'fo/foHome.html', {'flightOperator':flightOperator})

###############################################################################
def foSim(request, sim):
    simobj = Sim.objects.get(sim_name=sim)

    if request.method == 'POST':

        for subsystem in simobj.sys_list.all():
            if subsystem.sys_name in request.POST:
                form = SubsystemForm(request.POST, prefix=subsystem.sys_name, instance=subsystem)
                if form.is_valid():
                    form.save()

    forms = [SubsystemForm(prefix=subsystem.sys_name, instance=subsystem) for subsystem in simobj.sys_list.all()]
    return render(request, 'fo/foSim.html', {'sim': simobj, 'forms': forms})

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