from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.template import loader

#################### index#######################################
def index(request):
    return render(request, 'tc/index.html', {'title':'index'})
  
########### register here #####################################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            #TODO: implement account creation email confirmation
            ######################### mail system ####################################
            #htmly = get_template('fo/Email.html')
            #d = { 'username': username }
            #subject, from_email, to = 'welcome', 'chacotaco707@gmail.com', email
            #html_content = htmly.render(d)
            #msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            #msg.attach_alternative(html_content, "text/html")
            #msg.send()
            ##################################################################
            user = authenticate(request, username = username, password = password)
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('tcHome')
    else:
        form = UserRegisterForm()
    return render(request, 'tc/register.html', {'form': form, 'title':'register here'})
  
################ login forms###################################################
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('tcHome')
        else:
            messages.info(request, f'account does not exist')
    form = AuthenticationForm()
    return render(request, 'tc/login.html', {'form':form, 'title':'log in'})

def tcHome(request):
    template = loader.get_template('tc/tcHome.html')
    context = {}
    return HttpResponse(template.render(context, request))
def createSim(request):
    template = loader.get_template('tc/createSim.html')
    context = {}
    return HttpResponse(template.render(context, request))
