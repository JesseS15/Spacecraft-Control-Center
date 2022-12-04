from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegisterForm, SubsystemForm
from .models import FlightOperator
from tc.models import Sim

###############################################################################
def index(request):

    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('fo:home')
    else:
        return redirect('fo:login')

###############################################################################
def foRegister(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            # Send registration confirmation
            send_mail(
                'STaTE Registration',
                'Thank you, ' + username + ' for registering to STaTE!',
                None,
                [email],
                fail_silently=False,
            )
            user = authenticate(request, username = username, password = password)
            form = login(request, user)
            FlightOperator.objects.create(user = user)
            return redirect('fo:home')
    else:
        form = UserRegisterForm()

    return render(request, 'fo/foRegister.html', {'form': form, 'title':'register here'})

###############################################################################
def foLogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None and user.is_staff:
            return redirect('tc:login')
        if user is not None and not user.is_staff:
            form = login(request, user)
            return redirect('fo:home')
        else:
            messages.info(request, f'account does not exist')

    elif request.user.is_authenticated and not request.user.is_staff:
        return redirect('fo:home')

    form = AuthenticationForm()
    return render(request, 'fo/foLogin.html', {'form':form, 'title':'log in'})

###############################################################################
def foLogout(request):
    logout(request)
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