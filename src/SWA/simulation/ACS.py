from simulation.Subsystem import Subsystem
import random

class ACS(Subsystem):

    orientation = {
        "roll":0,
        "pitch":0,
        "yaw": 0
    }
    newOrientation = {
        "newRoll":0,
        "newPitch":0,
        "newYaw":0
    }

    rollActive = False
    pitchActive = False
    yawActive = False

    startLongitude = 0
    finalLongitude = 0
    currentLongitude = 0
    
    cmgStatus = False
    orientationRelay = False

    telemetryTransferComplete = False
    
    menu = ''
    commands = [
        "WELCOME TO THE ATTITUDE CONTROL SYSTEMS (ACS) CONSOLE",
        "Your task is to rotate the satellite for proper payload alignment with the imagery target on the earth’s surface",
        "1.) Longitude Check",
        "2.) Verify Alignment",
        "3.) CMG Activate Roll",
        "4.) CMG Activate Pitch",
        "5.) CMG Activate Yaw",
        "6.) Transfer Telemetry",
    ]
    consoleLog = []

    finalValues = {}

    def __init__(self, finalValues):
        super().__init__()
        self.orientation["roll"] = random.randint(-180,180)
        self.orientation["pitch"] = random.randint(-90,90)
        self.orientation["yaw"] = random.randint(-180,180)
        # setting starting longitude to random number from final longitude +50 to final longitude +90 (random magic numbers, dont be mad)
        self.startLongitude = random.randint(-180, 180)
        self.finalLongitude = finalValues["finalLongitude"]
        self.currentLongitude = self.startLongitude
        self.finalValues = finalValues

        self.menu = "tl" # can be tl, cmgRoll, cmgPitch, or cmgYaw
        
    def command(self, command):
        
        self.consoleLog.append("$ " + command)
        
        consoleResponse = []
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                consoleResponse.append("Checking Attitude Systems…")
                consoleResponse.append("The SimCraft’s current Longitude is: " + str(self.currentLongitude))
                consoleResponse.append("eta: " + str(self.longMin()) + " seconds until active range.")
            elif command_split[0] == "2":
                consoleResponse.append("Verifying Alignment...")
                consoleResponse.extend(self.verifyAlignment())
            elif command_split[0] == "3":
                consoleResponse.append("How much do you want to change the Roll by (in Degrees)?")
                self.menu = "cmgRoll"
            elif command_split[0] == "4":
                consoleResponse.append("How much do you want to change the Pitch by (in Degrees)?")
                self.menu = "cmgPitch"
            elif command_split[0] == "5":
                consoleResponse.append("How much do you want to change the Yaw by (in Degrees)?")
                self.menu = "cmgYaw"
            elif command_split[0] == "6":
                consoleResponse.append("Transfering ACS Telemetry...")
                consoleResponse.append( self.telemetryTransfer())
                consoleResponse.append("GREAT WORK ON THE ATTITUDE CONTROL SYSTEMS (ACS) CONSOLE!")
                #TODO: create instance where user cannot enter commands after subsys finished
            else:
                consoleResponse.append("Invalid Command " + command)

        elif self.menu == "cmgRoll":
            consoleResponse.append("The SimCraft's Roll had changed by " + str(self.newOrientation["newRoll"]))
            self.menu = "tl"
        
        elif self.menu == "cmgPitch":
            consoleResponse.append("The SimCraft's Pitch had changed by " + str(self.newOrientation["newPitch"]))
            self.menu = "tl"
        
        elif self.menu == "cmgYaw":
            consoleResponse.append("The SimCraft's Yaw had changed by " + str(self.newOrientation["newYaw"]))
            self.menu = "tl"
        
        else:
            self.menu = "tl"
        
        self.consoleLog.extend(consoleResponse)
        
        return self.consoleLog

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
        self.currentLongitude += 1
        if (self.currentLongitude == 180):
            self.currentLongitude = -180
        elif (self.currentLongitude == -180):
            self.currentLongitude = 180

    def longMin(self):
        if self.currentLongitude>81:
           return abs(self.finalLongitude - self.currentLongitude) + 180
        else:
            return abs(self.finalLongitude - self.currentLongitude)

    def checkLongitude(self):
        if (self.currentLongitude > (self.finalLongitude-15)) and (self.currentLongitude < (self.finalLongitude+15)):
            return True
        else:
            return False
        
    def update(self):
        self.updateRPY()
        self.updateLongitude()
    
    ############# CMG : User input updates ##############
    def updateRoll(self):
        if (newRoll > 10):
            newRoll = 10
        self.orientation['roll'] += newRoll
        return ("Roll updated by" + newRoll + "degrees")
    
    def updatePitch(self):
        if (newPitch > 10):
            newPitch = 10
        self.orientation['pitch'] += newPitch
        return ("Pitch updated by" + newPitch + "degrees")
    
    def updateYaw(self):
        if (newYaw > 10):
            newYaw = 10
        self.orientation['yaw'] += newYaw
        return ("Yaw updated by" + newYaw + "degrees")

    ###### Checking final orientation, passed from SimObject ###############
    def verifyAlignment(self):
        # Calculate required changes to roll, pitch and yaw
        rollDifference = self.finalValues["roll"] - self.orientation["roll"]
        pitchDifference = self.finalValues["pitch"] - self.orientation["pitch"]
        yawDifference = self.finalValues["yaw"] - self.orientation["yaw"]
        
        # Check if roll, pitch, and yaw are in acceptable range from final values
        if (abs(rollDifference) <= 10) and (abs(pitchDifference) <= 10) and (abs(yawDifference) <= 10):
            response = "The SimCraft's Alignment is Reached"
        else:
            response = ["The SimCraft's Alignment is not reached...",
                        "The roll is off by " + str(rollDifference),
                        "The Pitch is off by " + str(pitchDifference),
                        "The Yaw is off by " + str(yawDifference )]
        return response

    def systemChecks(self):
        align = self.verifyAlignment
        longitude = self.checkLongitude
        return align, longitude
    
    def telemetryTransfer(self):
        if (self.verifyAlignment and self.checkLongitude):
            self.telemetryTransferComplete = True
            return "Data has been Transferred!"
        else:
            self.telemetryTransferComplete = False
        return "Data Transfer Error! Attributes not within range."
            