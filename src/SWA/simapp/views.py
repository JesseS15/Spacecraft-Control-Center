from django.shortcuts import render
# Importing models from simaapp/views.py
from models import models
from .models import Buffer_Item, Sim

""" # Adding a command to the Command buffer thats in the Sim
def addItemToCommandBuffer(request):
    newItem = ''
    if (checkInput):
        cmd = models.new(Buffer_Item, buffer_item=newItem)
        Sim.command_buffer.add(cmd)
    else:
        return "****INVALID INPUT****"
    
def displayACSMenu(request):
    print(Sim.acs_subsys.main_menu)

def checkInput(menu, userInput):
    return True """
