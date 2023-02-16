# Manager for all of the missions. Will call MissionScript.py
# import in manage.py

#from tc.models import Sim
#from tc.views import createSim
import threading


def startThread():
    x = threading.Thread(target = thread_time)
    x.start()
    print("\n!!!! Thread started  !!!!\n")

# Adding new sim to the database
#def createNewSim(simName):
    #newSim = Sim.objects.create(sim_name = simName, sys1_name='ACS', sys2_name='TCS')
    #newSim.save()
    #createSim(sim_name = simName)
    #print('New Simulation created:' + simName)

#startThread()
#createNewSim("My new sim")