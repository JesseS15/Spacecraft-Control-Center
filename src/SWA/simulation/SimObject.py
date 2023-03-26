from simapp.models import Sim
from simulation.ACS import ACS
from simulation.TCS import TCS
from simulation.EPS import EPS
from simulation.COMMS import COMMS
from simulation.Dicts import Dicts
import threading
import time

class SimObject(threading.Thread):

    simName = ""
    mission = ""
    dictObject = Dicts()
    # Creats a new instance of the Attribute Dictionaries
    attributeDict = dictObject.dicts
    finalDict = dictObject.finalValues
    # All the subsystem objects
    subsystems = { "ACS": 0, "TCS": 0, "COMMS": 0, "EPS": 0 }

    def __init__(self, simName):
        threading.Thread.__init__(self)
        self.simName = simName
        print('\n  !!! NEW SIM', simName, 'CREATED !!!\n')

    # Method to update dictionaries. 
    def updateDictionaries(self, updateDict):
        self.dicts.update(updateDict)

    # Creating all the subsystems and passing them the dictionaries
    def createSubsys(self):
        self.subsystems["ACS"] = ACS(self.attributeDict)
        self.subsystems["EPS"] = EPS(self.attributeDict)
        self.subsystems["COMMS"] = COMMS(self.attributeDict)
        self.subsystems["TCS"] = TCS(self.attributeDict)

    def check(self):
        print('Sim Thread for '+ self.simName+' is reachable')

    def run(self):
        simobj = Sim.objects.get(sim_name = self.simName)
        simobj.sim_identifier = threading.get_ident()
        simobj.save()

        while True:
            print('thread ' + self.simName)
            print(threading.get_ident())
            time.sleep(5)