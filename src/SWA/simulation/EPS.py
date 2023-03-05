from Subsystem import Subsystem
import EPSSolarPanelCharging as Charging
import EPSInitializing as EPSStart
import EPSPowerDistribution as PD

class EPS(Subsystem):

    
    def __init__(self, dicts):
        super().__init__(dicts)
        print("New instance of EPS class created")

    def EPSStartup(inputWatts=200, period=3600):
        EPSStart.initialize(inputWatts)   #Takes input watts and buffer as an argument
        Charging.setupBatteries(period)
        PD.initialize(inputWatts)         #Takes input watts as an argument

    def requestPower(self, requestedPower, subsystemName):
        # Call method in the EPSPowerDistribution
        requestedPower = PD.requestPower(requestedPower, subsystemName)
        if requestedPower is None: return 0
        return requestedPower

    def powerDistributionError(self):
        print("Error with power distribution")

    def powerIntakeError(self):
        print("Error with power intake")

    def powerLevelError(self):
        print("Error with power level")

