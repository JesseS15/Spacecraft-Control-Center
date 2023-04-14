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

    telemetryTransferComplete = False

    longitudeValid = False
    rpyValid = False
    
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
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Attitude Systems...")
                time.sleep(5)
                self.consoleLog.append("The SimCraft’s current Longitude is: " + str(self.currentLongitude))
                self.consoleLog.append("eta: " + str(self.longMin()) + " seconds until active range.")
            elif command_split[0] == "2":
                self.consoleLog.append("Verifying Alignment...")
                time.sleep(5)
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
                time.sleep(5)
                self.consoleLog.append( self.telemetryTransfer())
                if (self.telemetryTransferComplete):
                    self.consoleLog.append("GREAT WORK ON THE ATTITUDE CONTROL SYSTEMS (ACS) CONSOLE!")
                #TODO: create instance where user cannot enter commands after subsys finished
            else:
                self.consoleLog.append("Invalid Command " + command)

        elif self.menu == "cmgRoll":
            self.consoleLog.append(self.updateRoll(int(command)))
            self.consoleLog.append("Roll can only be updated by 10 degrees at a time.")
            self.menu = "tl"
        
        elif self.menu == "cmgPitch":
            self.consoleLog.append(self.updatePitch(int(command)))
            self.consoleLog.append("Pitch can only be updated by 10 degrees at a time.")
            self.menu = "tl"
        
        elif self.menu == "cmgYaw":
            self.consoleLog.append(self.updateYaw(int(command)))
            self.consoleLog.append("Yaw can only be updated by 10 degrees at a time.")
            self.menu = "tl"
        
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
        if self.currentLongitude>81:
           return abs(self.finalLongitude - self.currentLongitude) + 180
        else:
            return abs(self.finalLongitude - self.currentLongitude)
        
    def update(self):
        self.updateRPY()
        self.updateLongitude()
    
    ############# CMG : User input updates ##############
    def updateRoll(self, newRoll):
        if (newRoll > 0):
            if(self.orientation['roll'] + newRoll >= 180):
                diff = self.orientation['roll'] + newRoll
                newDiff = -180 + diff
                self.orientation['roll'] = -180 + newDiff
            elif(self.orientation['roll'] + newRoll < 180):
                self.orientation['roll'] =+ newRoll
        if (newRoll < 0):
            if(self.orientation['roll'] + newRoll <= -180):
                diff = self.orientation['roll'] + newRoll
                newDiff = 180 + diff
                self.orientation['roll'] = 180 + newDiff
            elif(self.orientation['roll'] + newRoll > -180):
                self.orientation['roll'] =+ newRoll
        return ("Roll updated by " + str(newRoll) + " degrees")
    
    def updatePitch(self, newPitch):
        if (newPitch > 0):
            if(self.orientation['pitch'] + newPitch >= 90):
                diff = self.orientation['pitch'] + newPitch
                newDiff = -90 + diff
                self.orientation['pitch'] = -90 + newDiff
            elif(self.orientation['pitch'] + newPitch < 90):
                self.orientation['pitch'] =+ newPitch
        if (newPitch < 0):
            if(self.orientation['pitch'] + newPitch <= -90):
                diff = self.orientation['pitch'] + newPitch
                newDiff = 90 + diff
                self.orientation['pitch'] = 90 + newDiff
            elif(self.orientation['pitch'] + newPitch > -90):
                self.orientation['pitch'] =+ newPitch
        return ("Pitch updated by " + str(newPitch) + " degrees")
    
    def updateYaw(self, newYaw):
        if (newYaw > 0):
            if(self.orientation['yaw'] + newYaw >= 180):
                diff = self.orientation['yaw'] + newYaw
                newDiff = -180 + diff
                self.orientation['yaw'] = -180 + newDiff
            elif(self.orientation['yaw'] + newYaw < 180):
                self.orientation['yaw'] =+ newYaw
        if (newYaw < 0):
            if(self.orientation['yaw'] + newYaw <= -180):
                diff = self.orientation['yaw'] + newYaw
                newDiff = 180 + diff
                self.orientation['yaw'] = 180 + newDiff
            elif(self.orientation['yaw'] + newYaw > -180):
                self.orientation['yaw'] =+ newYaw
        return ("Yaw updated by " + str(newYaw) + " degrees")

    ###### Checking final orientation, passed from SimObject ###############
    def verifyAlignment(self):
        # Calculate required changes to roll, pitch and yaw
        #TODO change the differences to be actually accurate

        rollPosDif = abs(self.orientation["roll"] - self.finalValues["roll"])
        rollNegDif = 360 - abs(self.orientation["roll"] - self.finalValues["roll"])
        if rollNegDif<rollPosDif:
            rollDifference=rollNegDif
        else:
            rollDifference=rollPosDif

        pitchPosDif = abs(self.orientation["pitch"] - self.finalValues["pitch"])
        pitchNegDif = 180 - abs(self.orientation["pitch"] - self.finalValues["pitch"])
        if pitchNegDif<pitchPosDif:
            pitchDifference = pitchNegDif
        else:
            pitchDifference = pitchPosDif

        yawPosDif = abs(self.orientation["yaw"] - self.finalValues["yaw"])
        yawNegDif = 360 - abs(self.orientation["yaw"] - self.finalValues["yaw"])
        if yawNegDif<yawPosDif:
            yawDifference = yawNegDif
        else:
            yawDifference = yawPosDif

        
        #NOTE: the input can only change by 10 degrees and the correct range is within 10 degrees- theyre seperate values
        # Check if roll, pitch, and yaw are in acceptable range from final values
        if (abs(rollDifference) <= 15):
            response = ["The SimCraft's Roll Alignment is Reached"]
            self.rpyValid = True
        else:
            response = ["The roll is off by " + str(rollDifference)]
            self.rpyValid = False
        if (abs(pitchDifference) <= 15):
            response = ["The SimCraft's Pitch Alignment is Reached"]
        else:
            response = ["The Pitch is off by " + str(pitchDifference)]
            self.rpyValid = False
        if(abs(yawDifference) <= 15):
            response = ["The SimCraft's Yaw Alignment is Reached"]
        else:
            response = ["The Yaw is off by " + str(yawDifference )]
            self.rpyValid = False
        return response

    def checkLongitude(self):
        if (self.currentLongitude > (self.finalLongitude-15)) and (self.currentLongitude < (self.finalLongitude+15)):
            self.longitudeValid=True
            return True
        else:
            self.rpyValid=False
            return False

    def systemChecks(self):
        align = self.verifyAlignment()
        longitude = self.checkLongitude()
        return align, longitude
    
    def telemetryTransfer(self):
        if (self.rpyValid and self.longitudeValid):
            self.telemetryTransferComplete = True
            return "Data has been Transferred!"
        else:
            self.telemetryTransferComplete = False
        return "Data Transfer Error! Attributes not within range."
            