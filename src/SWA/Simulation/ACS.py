from Subsystem import Subsystem

class ACS(Subsystem):

    def __init__(self):
        super().__init__()
        altitude = 0.0
        orbit = 0.0
        orientation = [0,1,2]

    def thrustersError():
        return "Error with thrusters"

    def altitudeError():
        print("Altitude is not optimal")

    def orbitError():
        print("Not on correct orbit")

    def orientationError():
        print("Orientation incorrect")