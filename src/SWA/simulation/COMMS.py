from simulation.Subsystem import Subsystem
from simulation.Subsystem import EPS

class COMMS(Subsystem):

    def __init__(self, dicts):
        super().__init__(dicts)
        self.attributes = self.dicts['COMMS']
        print(self.dicts)


    def downlinkError(self):
        print("Error with the downlink")

    def uplinkError(self):
        print("Error with uplink")

    def antennaError(self):
        print("Error with antenna")

    def signalError(self):
        print("Signal is not clear")
