from simulation.Subsystem import Subsystem
import random

class ACS(Subsystem):

    orientation = {
        "roll":0,
        "pitch":0,
        "yaw": 0
    }

    telemetryTransferComplete = False
    startLongitude = 0
    finalLongitude = 0
    currentLongitude = 0

    def __init__(self, finalLongitude):
        super().__init__()
        self.orientation["roll"] = random.randint(-180,180)
        self.orientation["pitch"] = random.randint(-90,90)
        self.orientation["yaw"] = random.randint(-180,180)
        # setting starting longitude to random number from final longitude +50 to final longitude +90 (random magic numbers, dont be mad)
        self.startLongitude = random.randint(-180, 180)
        self.finalLongitude = finalLongitude
        self.currentLongitude = self.startLongitude
        self.prograde = bool(random.getrandbits(1))
        self.menu = "tl" # can be tl, cmgRoll, cmgPitch, or cmgYaw
        self.commandLog = []
        
        self.initializeCommandLog()
        
    def command(self, command):
        
        response = {
            'inputConsole' : self.commandLog,
            'outputConsole': [],
        }
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                pass
            elif command_split[0] == "2":
                pass
            elif command_split[0] == "3":
                self.menu = "cmgRoll"
                response['inputConsole'].append("How much do you want to change the Roll by (in Degrees)?")
            elif command_split[0] == "4":
                self.menu = "cmgPitch"
                response['inputConsole'].append("How much do you want to change the Pitch by (in Degrees)?")
            elif command_split[0] == "5":
                self.menu = "cmgYaw"
                response['inputConsole'].append("How much do you want to change the Yaw by (in Degrees)?")
            elif command_split[0] == "6":
                pass
            else:
                response['inputConsole'].append("Invalid Command " + command)

        elif self.menu == "cmgRoll":
            self.menu = "tl"
            self.appendCommandList()
        
        elif self.menu == "cmgPitch":
            self.menu = "tl"
            self.appendCommandList()
        
        elif self.menu == "cmgYaw":
            self.menu = "tl"
            self.appendCommandList()
        
        else:
            self.menu = "tl"
        
        return response

    def initializeCommandLog(self):
        self.commandLog.append("WELCOME TO THE ATTITUDE CONTROL SYSTEMS (ACS) CONSOLE")
        self.appendCommandList()
        return
    
    def appendCommandList(self):
        self.commandLog.append("1.) System Checks")
        self.commandLog.append("2.) Verify Alignment ")
        self.commandLog.append("3.) CMG Activate Roll")
        self.commandLog.append("4.) CMG Activate Pitch")
        self.commandLog.append("5.) CMG Activate Yaw")
        self.commandLog.append("6.) Transfer Telemetry")
        return

    def updateRPY(self):
        self.orientation["roll"] += random.randint(-1,1)
        if (self.orientation["roll"] > 180):
            self.orientation["roll"] = -179
        if (self.orientation["roll"] < -180):
            self.orientation["roll"] = 179

        self.orientation["pitch"] += random.randint(-1,1)
        if (self.orientation["pitch"] > 90):
            self.orientation["pitch"] = -89
        if (self.orientation["pitch"] < -90):
            self.orientation["pitch"] = 89

        self.orientation["yaw"] += random.randint(-1,1)
        if (self.orientation["yaw"] > 180):
            self.orientation["yaw"] = -179
        if (self.orientation["yaw"] < -180):
            self.orientation["yaw"] = 179

    def updateLongitude(self):
        if self.prograde:
            self.currentLongitude += 1
            if (self.currentLongitude == 180):
                self.currentLongitude = -180
        else:
            self.currentLongitude -= 1
            if (self.currentLongitude == -180):
                self.currentLongitude = 180

    def checkLongitude(self):
        if (self.currentLongitude == self.finalLongitude):
            return True
        else:
            return False
        
    def update(self):
        self.updateRPY()
    
    ############# CMG : User input updates ##############
    def updateRoll(self, newRoll):
        if (newRoll > 10):
            newRoll = 10
        self.orientation['roll'] += newRoll
        return ("Roll updated by" + newRoll + "degrees")
    
    def updatePitch(self, newPitch):
        if (newPitch > 10):
            newPitch = 10
        self.orientation['pitch'] += newPitch
        return ("Pitch updated by" + newPitch + "degrees")
    
    def updateYaw(self, newYaw):
        if (newYaw > 10):
            newYaw = 10
        self.orientation['yaw'] += newYaw
        return ("Yaw updated by" + newYaw + "degrees")

    ###### Checking final orientation, passed from SimObject ###############
    def verifyAlignment(self, finalValues):
        rollDifference = finalValues["roll"] - self.orientation["roll"]
        bitchDifference = finalValues["pitch"] - self.orientation["pitch"]
        yawDifference = finalValues["yaw"] - self.orientation["yaw"]
        if (abs(rollDifference) <= 10) and (abs(bitchDifference) <= 10) and (abs(yawDifference) <= 10):
            return True
        else:
            return False, rollDifference, bitchDifference, yawDifference

    def systemChecks(self):
        align = self.verifyAlignment
        longitude = self.checkLongitude
        return align, longitude
    
    def telemetryTransfer(self):
        if (self.verifyAlignment and self.checkLongitude):
            self.telemetryTransferComplete = True
        else:
            self.telemetryTransferComplete = False
        return self.telemetryTransferComplete
            