from django.http import HttpResponse
from django.template import loader


def login(request):
    template = loader.get_template('tc/login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def createSim(request):
    template = loader.get_template('tc/createSim.html')
    context = {}
    return HttpResponse(template.render(context, request))
