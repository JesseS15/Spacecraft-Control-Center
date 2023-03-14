from simulation.Dicts import Dicts

class MissionScript:

    missionName = ""

    # Defining a dictionary full of the subsystem dictionaries
    dicts = { "ACS": { }, "TCS": { }, "COMMS":{ }, "EPS":{ } }

    ####### CONSTRUCTOR ##########
    def __init__(self, mName):
        self.missionName = mName
        self.dicts = Dicts().dicts
        print("New Mission Script Created")  

    # Setting the starting values of the dictionaries for missions of this type
    def initalizeDicts(self):
        pass


