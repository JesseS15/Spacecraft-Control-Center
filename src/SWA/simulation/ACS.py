from Subsystem import Subsystem


class ACS(Subsystem):

    def __init__(self, dicts):
        super().__init__(dicts)
        

    def thrustersError(self):
        print(self.dicts["ACS"].get("isWorking"))
        print("Error with thrusters")

    def altitudeError(self):
        print("Altitude is not optimal")

    def orbitError(self):
        print("Not on correct orbit")

    def orientationError(self):
        print("Orientation incorrect")