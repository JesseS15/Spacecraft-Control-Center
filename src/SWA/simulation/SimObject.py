from simulation.MissionScript import MissionScript
from simulation.ACS import ACS
from simulation.TCS import TCS
from simulation.EPS import EPS
from simulation.COMMS import COMMS

class SimObject():

    simName = ""
    mission = ""
    # Defining a dictionary full of the subsystem dictionaries
    dicts = { "ACS": { }, "TCS": { }, "COMMS":{ }, "EPS":{ } }
    # All the subsystem objects
    subsystems = { "ACS": 0, "TCS": 0, "COMMS": 0, "EPS": 0 }

    def __init__(self, simName):
        self.simName = simName

    # Assinging a mission script to the sim
    # Setting dictionaries to the inital dictionaries set in the mission.
    def assignMissionScript(self, mName):
        self.mission = MissionScript(mName)
        self.dicts = self.mission.dicts
        self.createSubsys()

    # Method to update dictionaries. 
    def updateDictionaries(self, updateDict):
        self.dicts.update(updateDict)

    # Creating all the subsystems and passing them the dictionaries
    def createSubsys(self):
        self.subsystems["ACS"] = ACS(self.dicts)
        self.subsystems["EPS"] = EPS(self.dicts)
        self.subsystems["COMMS"] = COMMS(self.dicts)
        self.subsystems["TCS"] = TCS(self.dicts)

    def startSim(self):
        print("Starting " + self.simName + " simulation")

