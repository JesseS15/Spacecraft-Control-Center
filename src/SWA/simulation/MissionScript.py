from Dicts import Dicts

class MissionScript:

    missionName = ""

    # Defining a dictionary full of the subsystem dictionaries
    dicts = { "ACS": { }, "TCS": { }, "COMMS":{ }, "EPS":{ } }

    ####### CONSTRUCTOR ##########
    def __init__(self, mName):
        self.missionName = mName
        self.createDicts()
        print("New Mission Script Created")  

    # Creating the simulation dictionaries
    def createDicts(self):
        self.dicts = Dicts().dicts

    # Setting the starting values of the dictionaries for missions of this type
    def initalizeDicts(self):
        pass


