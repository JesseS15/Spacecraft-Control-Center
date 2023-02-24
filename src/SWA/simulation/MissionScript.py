from Dicts import Dicts

class MissionScript:

    # Defining a dictionary full of the subsystem dictionaries
    dicts = { "ACS": { }, "TCS": { }, "COMMS":{ }, "EPS":{ } }

    ####### CONSTRUCTOR ##########
    def __init__(self):
        self.createDicts
        print("New Mission Script Created")  

    # Creating the simulation dictionaries
    def createDicts(self):
        newDicts = Dicts()
        self.dicts = newDicts.dicts

    # Setting the starting values of the dictionaries for missions of this type
    def initalizeDicts(self):
        pass

        

