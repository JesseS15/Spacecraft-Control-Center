from Subsystem import Subsystem
class EPS(Subsystem):

    
    def __init__(self, dicts):
        super().__init__(dicts)
        print("New instance of EPS class created")
        

    def powerDistributionError(self):
        print("Error with power distribution")

    def powerIntakeError(self):
        print("Error with power intake")

    def powerLevelError(self):
        print("Error with power level")

