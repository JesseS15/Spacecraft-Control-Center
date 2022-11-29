from django.http import HttpResponse
from django.template import loader


def home(request):
    template = loader.get_template('home/home.html')
    context = {}
    return HttpResponse(template.render(context, request))

def contact(request):
    template = loader.get_template('home/contact.html')
    context = {}
    return HttpResponse(template.render(context, request))

def about(request):
    template = loader.get_template('home/about.html')
    context = {}
    return HttpResponse(template.render(context, request))
