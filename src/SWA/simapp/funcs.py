from simapp.models import Sim
from simulation.SimObject import SimObject
import random

def repopulateAllSimsDict(all_sims_dict):
    ## Repopulating the sim dictionary if it is empty and there are no sims in the dictionary
    sims = Sim.objects.all()
    if ((sims != None) and (len(all_sims_dict) == 0)):
        for s in sims:
            s_id = s.sim_identifier
            m = s.mission_script
            final_values = {}
            final_values["roll"] = m.final_roll
            final_values["pitch"] = m.final_pitch
            final_values["yaw"] = m.final_yaw
            all_sims_dict[s_id] = SimObject(final_values, pk=s.pk)
            all_sims_dict[s_id].start()
    print('\nAll Sims dictionary repopulated:')
    print(all_sims_dict,'\n')

def getUniqueValue(all_sims_dict):
    unique_number = random.randint(10000,50000)
    unique_check = False
    while (unique_check == False):
        if unique_number not in all_sims_dict:
            unique_check = True
    return unique_number



