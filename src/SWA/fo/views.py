from django.http import HttpResponse
from django.template import loader


def login(request):
    template = loader.get_template('fo/login.html')
    context = {}
    return HttpResponse(template.render(context, request))