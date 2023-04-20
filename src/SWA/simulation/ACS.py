import random
import time

class ACS():

    orientation = {
        "roll":0,
        "pitch":0,
        "yaw": 0
    }

    rollActive = False
    pitchActive = False
    yawActive = False

    startLongitude = 0
    finalLongitude = 0
    currentLongitude = 0
    
    cmgStatus = False
    orientationRelay = False

    telemetryTransfering = False
    telemetryTransferComplete = False

    longitudeValid = False
    rpyValid = False

    continueUpdates = True
    
    random.seed(9001)

    menu = ''
    commands = [
        "WELCOME TO THE ATTITUDE CONTROL SYSTEMS (ACS) CONSOLE",
        "Your task is to rotate the satellite for proper payload alignment with the imagery target on the earth’s surface",
        "Enter the command number in the console on the right to execute",
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
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Attitude Systems...")
                time.sleep(5)
                self.consoleLog.append("The SimCraft’s current Longitude is: " + str(self.currentLongitude) +"°")
                self.consoleLog.append("eta: " + str(self.longMin()) + " seconds until active range.")
            elif command_split[0] == "2":
                self.consoleLog.append("Verifying Alignment...")
                self.consoleLog.extend(self.verifyAlignment())
            elif command_split[0] == "3":
                self.consoleLog.append("How much do you want to change the Roll by (in Degrees)?")
                self.menu = "cmgRoll"
            elif command_split[0] == "4":
                self.consoleLog.append("How much do you want to change the Pitch by (in Degrees)?")
                self.menu = "cmgPitch"
            elif command_split[0] == "5":
                self.consoleLog.append("How much do you want to change the Yaw by (in Degrees)?")
                self.menu = "cmgYaw"
            elif command_split[0] == "6":
                self.consoleLog.append("Transfering ACS Telemetry...")
                self.consoleLog.append( self.telemetryTransfer())
                if (self.telemetryTransferComplete):
                    self.consoleLog.append("GREAT WORK ON THE ATTITUDE CONTROL SYSTEMS (ACS) CONSOLE!")
                #TODO: create instance where user cannot enter commands after subsys finished
            else:
                self.consoleLog.append("Invalid Command " + command)

        elif self.menu == "cmgRoll":
            self.consoleLog.append(self.updateRoll(int(command)))
            self.menu = "tl"
        
        elif self.menu == "cmgPitch":
            self.consoleLog.append(self.updatePitch(int(command)))
            self.menu = "tl"
        
        elif self.menu == "cmgYaw":
            self.consoleLog.append(self.updateYaw(int(command)))
            self.menu = "tl"

        elif self.menu == "done":
            self.consoleLog.append("ACS subsystem complete, console closed for commands")
        
        else:
            self.menu = "tl"
        
        return self.consoleLog

    def updateRPY(self):
        self.orientation["roll"] += random.randint(-2,2)
        if (self.orientation["roll"] > 180):
            self.orientation["roll"] = -179
        if (self.orientation["roll"] < -180):
            self.orientation["roll"] = 179

        self.orientation["pitch"] += random.randint(-2,2)
        if (self.orientation["pitch"] > 90):
            self.orientation["pitch"] = -89
        if (self.orientation["pitch"] < -90):
            self.orientation["pitch"] = 89

        self.orientation["yaw"] += random.randint(-2,2)
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
        desiredLongitude = 81
        if self.currentLongitude>desiredLongitude:
           return abs(self.finalLongitude - self.currentLongitude) + 180
        else:
            return abs(self.finalLongitude - self.currentLongitude)
        
    def update(self):
        if self.continueUpdates:
            self.updateRPY()
            self.updateLongitude()
    
    ############# CMG : User input updates ##############
    def updateRoll(self, newRoll):
        self.rollActive = True
        self.cmgStatus = True
        self.consoleLog.append("Please wait...")
        time.sleep(5)
        rollSum = newRoll + self.orientation['roll']
        self.rollActive = False
        self.cmgStatus = False
        if (rollSum < -180):
            self.orientation['roll'] = 360+rollSum
            return ("New roll = " + str(self.orientation['roll']))
        elif (rollSum > 180):
            self.orientation['roll'] = -360+rollSum
            return ("New roll = " + str(self.orientation['roll']))
        else:
            self.orientation['roll']=rollSum
            return ("New roll = " + str(self.orientation['roll']))


    def updatePitch(self, newPitch):
        self.pitchActive = True
        self.cmgStatus = True
        self.consoleLog.append("Please wait...")
        time.sleep(5)
        pitchSum = newPitch + self.orientation['pitch']
        self.pitchActive = False
        self.cmgStatus = False
        if (pitchSum < -90):
            self.orientation['pitch'] = 180+pitchSum
            return ("New pitch = " + str(self.orientation['pitch']))
        elif (pitchSum > 90):
            self.orientation['pitch'] = -180+pitchSum
            return ("New pitch = " + str(self.orientation['pitch']))
        else:
            self.orientation['pitch']=pitchSum
            return ("New pitch = " + str(self.orientation['pitch']))
        
    def updateYaw(self, newYaw):
        self.yawActive = True
        self.cmgStatus = True
        self.consoleLog.append("Please wait...")
        time.sleep(5)
        yawSum = newYaw + self.orientation['yaw']
        self.yawActive = False
        self.cmgStatus = False
        if (yawSum < -180):
            self.orientation['yaw'] = 360+yawSum
            return ("New yaw = " + str(self.orientation['yaw']))
        elif (yawSum > 180):
            self.orientation['yaw'] = -360+yawSum
            return ("New yaw = " + str(self.orientation['yaw']))
        else:
            self.orientation['yaw']=yawSum
            return ("New yaw = " + str(self.orientation['yaw']))

    ###### Checking final orientation, passed from SimObject ###############
    def verifyAlignment(self):
        # Calculate required changes to roll, pitch and yaw
        acceptableRange = 15

        rollPosDif = abs(self.orientation["roll"] - self.finalValues["roll"])
        if rollPosDif > 180:
            rollDif = 360 - rollPosDif
        else: 
            rollDif=rollPosDif


        pitchPosDif = abs(self.orientation["pitch"] - self.finalValues["pitch"])
        if pitchPosDif>90:
            pitchDif = 180 - pitchPosDif
        else:
            pitchDif=pitchPosDif

        yawPosDif = abs(self.orientation["yaw"] - self.finalValues["yaw"])
        if yawPosDif>180:
            yawDif = 360 - yawPosDif
        else:
            yawDif=yawPosDif

        # Check if roll, pitch, and yaw are in acceptable range from final values
        output = []
        if (abs(rollDif) <= acceptableRange):
            output.append("The SimCraft's Roll Alignment is Reached")
            self.rpyValid = True
        else:
            output.append("The roll is off by " + str(rollDif) +"°")
            self.rpyValid = False

        if (abs(pitchDif) <= acceptableRange):
            output.append("The SimCraft's Pitch Alignment is Reached")
        else:
            output.append("The Pitch is off by " + str(pitchDif) +"°")
            self.rpyValid = False

        if(abs(yawDif) <= acceptableRange):
            output.append("The SimCraft's Yaw Alignment is Reached")
        else:
            output.append("The Yaw is off by " + str(yawDif) +"°")
            self.rpyValid = False
        return output

    def checkLongitude(self):
        acceptableRange=15
        if (self.currentLongitude > (self.finalLongitude-acceptableRange)) and (self.currentLongitude < (self.finalLongitude+acceptableRange)):
            self.longitudeValid=True
            return True
        else:
            self.rpyValid=False
            return False
    
    def telemetryTransfer(self):
        if (self.rpyValid and self.longitudeValid):
            self.telemetryTransfering = True
            self.consoleLog.append("Please wait...")
            time.sleep(5)
            self.telemetryTransfering = False
            self.telemetryTransferComplete = True
            self.menu = "done"
            self.continueUpdates = False
            return "Data has been Transferred!"
        else:
            self.telemetryTransferComplete = False
        return "Data Transfer Error! Attributes not within range."
            