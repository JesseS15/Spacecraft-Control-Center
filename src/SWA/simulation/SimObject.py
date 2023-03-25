from simulation.ACS import ACS
from simulation.TCS import TCS
from simulation.EPS import EPS
from simulation.COMMS import COMMS
from simulation.Dicts import Dicts

class SimObject():

    simName = ""
    mission = ""
    dictObject = Dicts()
    # Creats a new instance of the Attribute Dictionaries
    attributeDict = dictObject.dicts
    finalDict = dictObject.finalValues

    # All the subsystem objects
    subsystems = { "ACS": 0, "TCS": 0, "COMMS": 0, "EPS": 0 }

    def __init__(self, simName):
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

    def startSim(self):
        print("Starting " + self.simName + " simulation")

