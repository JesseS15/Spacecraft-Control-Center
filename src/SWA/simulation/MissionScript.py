from ACS import ACS
from TCS import TCS
from EPS import EPS
from COMMS import COMMS
from Dicts import ACSDict
from Dicts import TCSDict
from Dicts import EPSDict
from Dicts import COMMSDict

class MissionScript:

    # Defining a dictionary full of the subsystem dictionaries
    dicts = { "ACS": { }, "TCS": { }, "COMMS":{ }, "EPS":{ } }
    # All the subsystem objects
    subsystems = { "ACS": 0, "TCS": 0, "COMMS": 0, "EPS": 0 }

    # Creating all the simulation dictionaries
    def createSimDicts(self):
        # Setting the dicts dictionary to a copy, dict(ACSDict), of each subsystem dictionary that is imported
        self.dicts["ACS"] = dict(ACSDict)
        self.dicts["TCS"] = dict(TCSDict)
        self.dicts["EPS"] = dict(EPSDict)
        self.dicts["COMMS"] = dict(COMMSDict)

    # Creating all the subsystems and passing them the dictionaries
    def createSubsys(self):
        self.subsystems["ACS"] = ACS(self.dicts)
        self.subsystems["EPS"] = EPS(self.dicts)
        self.subsystems["COMMS"] = COMMS(self.dicts)
        self.subsystems["TCS"] = TCS(self.dicts)

    ####### CONSTRUCTOR ##########
    def __init__(self):
        print("New Mission Script Created")
        self.createSimDicts()
        self.createSubsys()

    # Method to update dictionaries. 
    # May need to just put dictionaries in a class and handle it that way?
    def updateDictionaries(self, updateDict):
        self.dicts.update(updateDict)

    # Method to test interactions (NOT SURE IF IT STILL WORKS)
    def printSomething(self):
        # Testing dictionary updates
        print(self.dictionaries["ACS"].get("isWorking"))
        self.dictionaries["ACS"]["isWorking"] = True
        print(self.dictionaries["ACS"].get("isWorking"))
        self.subsystems["ACS"].thrustersError()

    # Method to start the mission (will need to actually create once a missions script is aquired)
    def startM(self):
        print("Starting mission")
        

