# Manager for all of the missions. Will call MissionScript.py

import threading
from SimObject import SimObject

# SimManager manages all the sims for A CLASS
# An instance needs to be created when a new class (of students) is made
class SimManager:

    # Dictionary to hold all the simulations
    className = ""

    def __init__(self, className):
        print("New SimManager instance created")
        self.className = className              

    ########### Do these need to be called here? #####################
    # Method that starts a given name simulation
    def startASim(self,sName):
        self.simulation[sName].startSim()
        print("\n!!!! Thread started  !!!!\n")
    ##################################################################


