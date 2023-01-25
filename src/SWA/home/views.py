from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegisterForm
from fo.models import FlightOperator

###############################################################################
def index(request):
    template = loader.get_template('home/home.html')
    context = {}
    return HttpResponse(template.render(context, request))

###############################################################################
def contact(request):
    template = loader.get_template('home/contact.html')
    context = {}
    return HttpResponse(template.render(context, request))

###############################################################################
def about(request):
    template = loader.get_template('home/about.html')
    context = {}
    return HttpResponse(template.render(context, request))

###############################################################################
def userLogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        form = login(request, user)

        if user is not None and user.is_staff:
            return redirect('tc:home')
        if user is not None and not user.is_staff:
            return redirect('fo:home')
        else:
            messages.info(request, f'account does not exist')

    elif request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('tc:home')
        if not request.user.is_staff:
            return redirect('fo:home')

    form = AuthenticationForm()
    return render(request, 'home/login.html', {'form':form, 'title':'STaTE Login'})

###############################################################################
def userLogout(request):
    logout(request)
    return redirect('home:login')

###############################################################################
def register(request):

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

    return render(request, 'home/register.html', {'form': form, 'title':'STaTE Register'})
