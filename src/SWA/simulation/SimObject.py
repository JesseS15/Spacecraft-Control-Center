from simapp.models import Sim
from simulation.ACS import ACS
from simulation.TCS import TCS
from simulation.EPS import EPS
from simulation.COMMS import COMMS
from simulation.payload import payload
import threading
import time
import random

class SimObject(threading.Thread):

    finalValues = {
		"roll": 0,
		"pitch": 0,
		"yaw": 0,
		"finalLongitude": 81
	}

    simName = ""
    pk = 0
    
    # All the subsystem objects
    subsystems = { "ACS": 0, "TCS": 0, "COMMS": 0, "EPS": 0, "Payload": 0 }

    telemetry = {"ACS": False, "TCS": False, "EPS": False, "Payload": False}

    def __init__(self, final_values, pk):
        threading.Thread.__init__(self)
        #self.finalValues = final_values
        sim = Sim.objects.get(pk = pk)
        self.pk = sim.pk
        self.simName = sim.sim_name
        self.createSubsys(sim)
        print('\n  !!! NEW SIM', self.simName, 'CREATED !!!\n')

    # Creating all the subsystems and passing them the dictionaries
    def createSubsys(self, sim):
        self.subsystems["ACS"] = ACS(self.finalValues["finalLongitude"])
        
        #self.subsystems["EPS"] = EPS()
        #self.subsystems["COMMS"] = COMMS()
        #self.subsystems["TCS"] = TCS()
        #self.subsystems["Payload"] = payload()

    def checkTelemetry(self):
        self.telemetry["ACS"] = self.subsystems["ACS"].telemetryTransfer()

    def check(self):
        print('Sim Thread for '+ self.simName+' is reachable')

    def update(self):
        self.subsystems["ACS"].update()
        self.subsystems["EPS"].update()
        self.subsystems["TCS"].update()
        self.subsystems["COMMS"].update()
        self.subsystems["Payload"].update()

    def run(self):
        simobj = Sim.objects.get(pk = self.pk)
        simobj.sim_identifier = threading.get_ident()
        simobj.save()

        while True:
            print('thread ' + self.simName)
            print(threading.get_ident())
            #Probably put stuff in this block under self.update function 
            self.update()
            self.telemetry = self.subsystems["ACS"].updateRPY()
            
            #End block here
            time.sleep(5)