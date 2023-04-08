from simapp.models import Sim, DisplayBufferItem
from simulation.ACS import ACS
from simulation.TCS import TCS
from simulation.EPS import EPS
from simulation.COMMS import COMMS
from simulation.Dicts import Dicts
from simulation.payload import payload
import threading
import time
import random

class SimObject(threading.Thread):

    simName = ""
    mission = ""
    pk = 0
    dictObject = Dicts()
    # Creats a new instance of the Attribute Dictionaries
    attributeDict = dictObject.dicts
    finalDict = dictObject.finalValues
    # All the subsystem objects
    # what the heck is all this for??? v
    # subsystems = { "ACS": 0, "TCS": 0, "COMMS": 0, "EPS": 0 }

    telemetry = {"ACS": False, "TCS": False, "EPS": False, "payload": False}
    orientation = {"roll": 0, "pitch": 0, "yaw": 0}

    def __init__(self, pk):
        threading.Thread.__init__(self)
        sim = Sim.objects.get(pk = pk)
        self.pk = sim.pk
        self.simName = sim.sim_name
        self.telemetry["roll"]=random.randint(-180,180)
        self.telemetry["pitch"]=random.randint(-90,90)
        self.telemetry["yaw"]=random.randint(-180,180)

        # self.createSubsys() ### this is will be replaced with normal variables in init

        print('\n  !!! NEW SIM', self.simName, 'CREATED !!!\n')

    # Method to update dictionaries. 
    def updateDictionaries(self, updateDict):
        self.dicts.update(updateDict)

    # Creating all the subsystems and passing them the dictionaries
    # This will likely be deleted
    """ def createSubsys(self):
        self.subsystems["ACS"] = ACS(self.attributeDict)
        self.subsystems["EPS"] = EPS(self.attributeDict)
        self.subsystems["COMMS"] = COMMS(self.attributeDict)
        self.subsystems["TCS"] = TCS(self.attributeDict)
    """

    def check(self):
        print('Sim Thread for '+ self.simName+' is reachable')

    def update(self):
        ACS.update()
        EPS.update()
        TCS.update()
        COMMS.update()
        #TODO Add payload to simobject
        #payload.update()

    def run(self):
        simobj = Sim.objects.get(pk = self.pk)
        simobj.sim_identifier = threading.get_ident()
        simobj.save()

        while True:
            print('thread ' + self.simName)
            print(threading.get_ident())
            #self.update()
            #Probably put stuff in this block under self.update function 
            self.telemetry = ACS.updateRPY(self.telemetry)
            
            #End block here

            displayobj = DisplayBufferItem.objects.create(buffer_item = self.simName + " updates")
            displayobj.save()
            simobj.display_buffer.add(displayobj)
            time.sleep(5)