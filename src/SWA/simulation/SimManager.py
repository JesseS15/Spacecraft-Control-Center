# Manager for all of the missions. Will call MissionScript.py

import threading
from MissionScript import MissionScript


class SimManager:

    # Dictionary to hold all the simulations
    simulations = { }

    def __init__(self):
        print("New SimManager instance created")              

    # Pass a name for the simulation and a new MissionScript (simulation) will be created
    def createSimulation(self,name):
        # Need to start a thread here
        self.simulations[name] = MissionScript()
        print("New MissionScript object created in SWA\Simulation\SimManager.py createSimulation() method")

    # Method that starts a given name simulation
    def startAMission(self,name):
        x = threading.Thread(target = self.simulations[name].startM())
        x.start()
        print("\n!!!! Thread started  !!!!\n")

    # Method that starts ALL the missions startM() method for all missions
    def startAllMissions(self):
        for mission in self.simulations:
            self.startAMission(mission)



sm = SimManager()
sm.createSimulation("Sim1")
sm.createSimulation("Sim2")
sm.startAllMissions()



##### ALL THE STUFF FROM EARLIER ##########
# Adding new sim to the database
#def createNewSim(simName):
    #newSim = Sim.objects.create(sim_name = simName, sys1_name='ACS', sys2_name='TCS')
    #newSim.save()
    #createSim(sim_name = simName)
    #print('New Simulation created:' + simName)

#startThread()
#createNewSim("My new sim")