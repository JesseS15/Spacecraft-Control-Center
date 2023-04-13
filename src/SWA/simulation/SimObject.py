from simapp.models import Sim
from simulation.ACS import ACS
from simulation.TCS import TCS
from simulation.EPS import EPS
from simulation.COMMS import COMMS
from simulation.Payload import Payload
import threading
import time
import random

class SimObject(threading.Thread):

    finalValues = {
		"roll": 0,
		"pitch": 0,
		"yaw": 0,
		"finalLongitude": 0
	}

    simName = ""
    pk = 0
    
    # Dictionary to hold all the subsystem objects
    subsystems = { "ACS": 0, "TCS": 0, "COMMS": 0, "EPS": 0, "Payload": 0 }

    telemetry = {"ACS": False, "TCS": False, "EPS": False, "Payload": False}

    def __init__(self, final_values, pk):
        threading.Thread.__init__(self)
        self.finalValues = final_values

        # Longitude of 81 is ERAU Daytona Beach campus
        self.finalValues["finalLongitude"] = 81

        sim = Sim.objects.get(pk = pk)
        self.pk = sim.pk
        self.simName = sim.sim_name
        self.createSubsys()
        print('\n  !!! NEW SIM', self.simName, 'CREATED !!!\n')

    # Creating all the subsystem objects and adding them to the subsystem dictionary
    def createSubsys(self):
        self.subsystems["ACS"] = ACS(self.finalValues)
        self.subsystems["EPS"] = EPS()
        self.subsystems["COMMS"] = COMMS()
        self.subsystems["TCS"] = TCS()
        self.subsystems["Payload"] = Payload()

    def checkTelemetry(self):
        # Using flag telemetryTransferComplete rather than calling function (that is for user command)
        self.telemetry["ACS"] = self.subsystems["ACS"].telemetryTransferComplete
        self.telemetry["EPS"] = self.subsystems["EPS"].telemetryTransferComplete
        self.telemetry["TCS"] = self.subsystems["TCS"].telemetryTransferComplete
        self.telemetry["Payload"] = self.subsystems["Payload"].telemetryTransferComplete

    def checkPayloadReady(self):
        acs = self.telemetry["ACS"]
        eps = self.telemetry["EPS"]
        tcs = self.telemetry["TCS"]
        long = self.subsystems["ACS"].checkLongitude()
        if acs and eps and tcs and long:
            self.subsystems["Payload"].ready = True

    def check(self):
        print('Sim Thread for '+ self.simName+' is reachable')

    def update(self):
        # Checking payload is good to take picture
        self.checkPayloadReady()
        self.subsystems["COMMS"].allTelemetryData = self.telemetry
        self.subsystems["ACS"].update()
        self.subsystems["EPS"].update()
        self.subsystems["TCS"].update()
        self.subsystems["COMMS"].update()

    def run(self):
        simobj = Sim.objects.get(pk = self.pk)
        simobj.sim_identifier = threading.get_ident()
        simobj.save()

        while True:
            print('thread ' + self.simName)
            print(threading.get_ident())
            #Probably put stuff in this block under self.update function 
            self.update()
            
            #End block here
            time.sleep(5)