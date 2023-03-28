from simulation.Subsystem import Subsystem
import random

class ACS(Subsystem):

    def __init__(self, dicts):
        self.dicts = dicts
        print("New instance of ACS class created")

    def randomRollPitchYaw(self):
        self.roll += random.randint(-10,10)
        self.pitch += random.randint(-10,10)
        self.yaw += random.randint(-10,10)
    
    def userChosenRllPitchYaw(self, r, p, y):
        self.roll = r
        self.pitch = p
        self.yaw = y
        return "Roll/Pitch/Yaw updated"
    
    def updateRoll(self, newRoll):
        self.roll = newRoll
        return ("Roll updated by" + newRoll + "degrees")
    
    def updatePitch(self, newPitch):
        self.pitch = newPitch
        return ("Pitch updated by" + newPitch + "degrees")
    
    def updateYaw(self, newYaw):
        self.yaw = newYaw
        return ("Yaw updated by" + newYaw + "degrees")

    def update():
        ACS.randomRollPitchYaw()


    def checkFinalRPY(self):
        if ((self.roll == self.finalRoll) and 
            (self.pitch == self.finalPitch) and 
            (self.yaw == self.finalYaw)):
            return True
        else: 
            return False

    def sendTelemetry(self):
        pass

    def verifySignalStatus():
        return True




    
        


    