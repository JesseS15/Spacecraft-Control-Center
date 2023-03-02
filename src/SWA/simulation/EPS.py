from Subsystem import Subsystem
import EPSSolarPanelCharging
import EPSInitializing
import EPSPowerDistribution

class EPS(Subsystem):

    
    def __init__(self, dicts):
        super().__init__(dicts)
        print("New instance of EPS class created")

    def requestPower(self):
        # Call method in the EPSPowerDistribution
        pass    

    def powerDistributionError(self):
        print("Error with power distribution")

    def powerIntakeError(self):
        print("Error with power intake")

    def powerLevelError(self):
        print("Error with power level")

