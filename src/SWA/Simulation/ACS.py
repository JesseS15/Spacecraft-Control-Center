class ACS(Subsystem):

    altitude = 0.0
    orbit = 0.0
    orientation = [0,1,2]

    def thrustersErro():
        print("Error with thrusters")

    def altitudeError():
        print("Altitude is not optimal")

    def orbitError():
        print("Not on correct orbit")

    def orientationError():
        print("Orientation incorrect")