from simulation.Subsystem import Subsystem
import random

class TCS(Subsystem):
    #TODO THIS should be changed in the future I believe, needs to be able to handle all subsystem's temps
    def __init__(self, dicts):
        super().__init__(dicts)
        self.checks = {'Heating Elements' : random.choice([True, False]),
                       'Bus Connection' : random.choice([True, False]),
                       'Telemetry Signal' : random.choice([True, False])}
        self.allChecks = False
        self.verifyStatus = False

    def regulationFunction(self):
        print("Function to regulate tempurature")

    def regulationError(self):
        print("Error with tempurature regulation in TCS")

<<<<<<< Updated upstream
    def update():
        pass
=======
    #TCS Console commands ##############################################
    def systemChecks(self):
        badChecks = [key for key, value in self.checks.items() if not value]
        if not badChecks:
            print("No errors found")
            self.allChecks = True
        else:
            print("ERROR FOUND with :")
            for key,value in badChecks:
                print(key)
            print("Enter refresh to reset the system and re-start system checks")
        print("Enter 'go' if all systems are ready")

    def refresh(self):
        self.checks = {key: True for key in self.checks}

    def verify(self):
        if not self.allChecks:
            print('All system checks not completed')
            return
        print("Verifying Spacecraft thermal level. Please wait .....")
        self.verifyStatus = True
        print("Verifying Thermals...")
        
    
>>>>>>> Stashed changes
