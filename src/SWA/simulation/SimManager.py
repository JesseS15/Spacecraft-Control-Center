# Manager for all of the missions. Will call MissionScript.py

import threading
from SimObject import SimObject

# SimManager manages all the sims for A CLASS
# An instance needs to be created when a new class (of students) is made
class SimManager:

    # Dictionary to hold all the simulations
    simulations = { }
    className = ""

    def __init__(self, className):
        print("New SimManager instance created")
        self.className = className              

    # Pass a name for the simulation and a new MissionScript (simulation) will be created
    def createSimulation(self,simName):
        self.simulations[simName] = SimObject(simName)
        print("New SimObject created in SWA\Simulation\SimManager.py createSimulation() method")


    ########### Do these need to be called here? #####################
    # Method that starts a given name simulation
    def startASim(self,sName):
        self.simulation[sName].startSim()
        print("\n!!!! Thread started  !!!!\n")

    # Method that starts ALL the missions startM() method for all missions
    def startAllSims(self):
        for sim in self.simulations:
            self.startASim(sim)
    ##################################################################

sm = SimManager()
sm.createSimulation("Sim1")
sm.createSimulation("Sim2")



##### ALL THE STUFF FROM EARLIER ##########
# Adding new sim to the database
#def createNewSim(simName):
    #newSim = Sim.objects.create(sim_name = simName, sys1_name='ACS', sys2_name='TCS')
    #newSim.save()
    #createSim(sim_name = simName)
    #print('New Simulation created:' + simName)

#startThread()
#createNewSim("My new sim")