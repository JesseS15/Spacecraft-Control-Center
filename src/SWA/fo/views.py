from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegisterForm, SubsystemForm, JoinClassForm
from .models import FlightOperator, Post, Like
from tc.models import Sim, Class, Subsystem

from django.http import JsonResponse
from django.template.loader import render_to_string
import json

def post(request):
    posts = Post.objects.all()  # Getting all the posts from database
    return render(request, 'fo/post.html', { 'posts': posts })

def submit(request):
    if request.method == 'GET':
           post_id = request.GET['post_id']
           post_text = request.GET['post_text']
           likedpost = Post.objects.get(pk=post_id) #getting the liked posts
           likedpost.post_heading = post_text
           likedpost.save()
           m = Like(post=likedpost) # Creating Like Object
           m.save()  # saving it to store in database
           return HttpResponse(likedpost.post_heading) # Sending an success response
    else:
           return HttpResponse("Request method is not a GET")

def fetchdata(request, simkey):
    if request.method == 'GET':
        dic = {}
        simobj = Sim.objects.get(pk = simkey)
        for sys in simobj.sys_list.all():
            dic.update({sys.sys_name : sys.button_value})
        return HttpResponse(json.dumps(dic)) # Sending an success response
    else:
        return HttpResponse("Request method is not GET")

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
def foSim(request, simkey):
    simobj = Sim.objects.get(pk=simkey)

    return render(request, 'fo/foSim.html', {'sim': simobj, 'simkey': simkey})

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