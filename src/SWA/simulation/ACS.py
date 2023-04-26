# STaTE
# File: ACS.py 
# Purpose: Define ACS subsytem for use in a SimObject thread

import random
import time

class ACS():
    
    ################### INITIALIZE ACS SUBSYTEM #######################
    def __init__(self, finalValues):
        super().__init__()
        self.finalValues = {
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "finalLongitude": 0
        }
        self.finalValues = finalValues
        
        self.orientation = {
            "roll": 0,
            "pitch": 0,
            "yaw": 0
        }
        self.orientation["roll"] = random.randint(-180,180)
        self.orientation["pitch"] = random.randint(-90,90)
        self.orientation["yaw"] = random.randint(-180,180)

        self.rollActive = False
        self.pitchActive = False
        self.yawActive = False

        self.startLongitude = random.randint(-180, 180)
        self.finalLongitude = finalValues["finalLongitude"]
        self.currentLongitude = self.startLongitude
        # Randomly chosen update amount to keep simulation time shorter
        self.longitudeUpdateAmount = 5
        
        self.cmgStatus = False
        self.orientationRelay = False

        self.telemetryTransferring = False
        self.telemetryTransferComplete = False

        self.longitudeValid = False
        self.rpyValid = False

        self.continueUpdates = True
        
        random.seed(9001)

        # Console infastructure
        self.menu = "tl" # can be tl, cmgRoll, cmgPitch, or cmgYaw
        self.commands = [
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
        self.consoleLog = []
        
    ################### ACS CONSOLE COMMANDS #######################
    def command(self, command):
        self.consoleLog.append("$ " + command)
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Attitude Systems...")
                time.sleep(3)
                self.consoleLog.extend(self.checkAttitudeSystems())
            elif command_split[0] == "2":
                self.consoleLog.append("Verifying Alignment...")
                time.sleep(3)
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
                self.consoleLog.append("Transferring ACS Telemetry...")
                self.consoleLog.extend(self.telemetryTransfer())
            else:
                self.consoleLog.append("Invalid Command: " + command)

        elif self.menu == "cmgRoll":
            self.consoleLog.append(self.updateRollOrYaw(int(command), "roll"))
            self.menu = "tl"
        
        elif self.menu == "cmgPitch":
            self.consoleLog.append(self.updatePitch(int(command)))
            self.menu = "tl"
        
        elif self.menu == "cmgYaw":
            self.consoleLog.append(self.updateRollOrYaw(int(command), "yaw"))
            self.menu = "tl"

        elif self.menu == "done":
            self.consoleLog.append("ACS subsystem complete, console closed for commands")
        
        else:
            self.menu = "tl"
        
        return self.consoleLog
    
    # tl menu option 1
    def checkAttitudeSystems(self):
        output = []
        output.append("The SimCraft’s current Longitude is: " + str(self.currentLongitude) +"°")
        output.append(self.longitudeETASeconds())
        return output
    
    # Method to determine how many seconds until longitude is within range
    def longitudeETASeconds(self):
        if (self.longitudeValid):
            return ("Longitude within acceptable range. Transfer Telemetry to complete subsystem.")
        else:
            if self.currentLongitude > self.finalLongitude:
                eta = abs(360+self.finalLongitude-self.currentLongitude)#/self.longitudeUpdateAmount
            else:
                eta = abs(self.finalLongitude - self.currentLongitude)#/self.longitudeUpdateAmount
            return ("ETA: " + str(eta) + " seconds until active range.")
        
    # tl menu option 2
    def verifyAlignment(self):
        output = []
        acceptableRange = 15
        self.rpyValid = True
        for item in self.orientation:
            itemDif = abs(self.orientation[item] - self.finalValues[item])
            if (item == "pitch"):
                if (itemDif > 90):
                    itemDif = 180 - itemDif
            elif (itemDif > 180):
                    itemDif = 360 - itemDif
            if (abs(itemDif) <= acceptableRange):
                output.append("..." + str.capitalize(item) + " Alignment -- REACHED")
            else:
                output.append("..." + str.capitalize(item) + " Alignment -- NOT REACHED -- OFF BY: " + str(itemDif) + "°") 
                self.rpyValid = False
        return output
    
    # tl menu options 3, 4, 5:
    # Transfer to cmgRoll, cmgPitch, or cmgYaw menu respectively
    
    # tl menu option 6
    def telemetryTransfer(self):
        output = []
        if (self.rpyValid and self.longitudeValid):
            self.telemetryTransferring = True
            output.append("Please wait...")
            time.sleep(3)
            self.telemetryTransferring = False
            self.telemetryTransferComplete = True
            self.menu = "done"
            self.continueUpdates = False
            output.append("...Data Transfer -- COMPLETE!")
            output.append("GREAT WORK ON THE ATTITUDE CONTROL SYSTEMS (ACS) CONSOLE!")
        else:
            self.telemetryTransferComplete = False
            output.append("!!Data Transfer -- ERROR!!")
            if (not self.rpyValid): 
                output.append("...Alignment -- OUT OF RANGE -- Run Verify Alignment to check")
            else: 
                output.append("...Alignment -- IN RANGE")
            if (not self.longitudeValid): 
                output.append("...Longitude -- NOT REACHED -- Run Longitude Check for ETA")
            else: 
                output.append("...Longitude -- REACHED")
        return output
    
    #CMG : User input updates
    # cmgRoll/cmgYaw menu option
    def updateRollOrYaw(self, newValue, item):
        if (item == "roll"):
            self.rollActive = True
        else:
            self.yawActive = True
        self.cmgStatus = True
        self.consoleLog.append("Please wait...")
        time.sleep(3)
        itemSum = newValue + self.orientation[item]
        if (item == "roll"):
            self.rollActive = False
        else:
            self.yawActive = False
        self.cmgStatus = False
        if (itemSum < -180):
            self.orientation[item] = 360+itemSum
        elif (itemSum > 180):
            self.orientation[item] = -360+itemSum
        else:
            self.orientation[item]=itemSum
        return ("..." + str.capitalize(item) + " Alignment -- RESET TO " + str(self.orientation[item]) + "°")

    # cmgPitch menu option
    def updatePitch(self, newPitch):
        self.pitchActive = True
        self.cmgStatus = True
        self.consoleLog.append("Please wait...")
        time.sleep(3)
        pitchSum = newPitch + self.orientation['pitch']
        self.pitchActive = False
        self.cmgStatus = False
        if (pitchSum < -90):
            self.orientation['pitch'] = 180+pitchSum
        elif (pitchSum > 90):
            self.orientation['pitch'] = -180+pitchSum
        else:
            self.orientation['pitch']=pitchSum
        return ("Pitch Alignment -- RESET TO " + str(self.orientation['pitch']) + "°")

    ################### ACS UPDATE #######################
    def update(self):
        if self.continueUpdates:
            self.updateRPY()
            self.updateLongitude()
            self.checkLongitude()
            
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
        self.currentLongitude += self.longitudeUpdateAmount
        if (self.currentLongitude != 0):
            if ((180 % self.currentLongitude) == 180):
                self.currentLongitude = -180 + (self.currentLongitude % 180)
            elif ((-180 % self.currentLongitude) == -180):
                self.currentLongitude = 180 + (self.currentLongitude % -180)

    def checkLongitude(self):
        acceptableRange = 25
        if (self.currentLongitude >= (self.finalLongitude-acceptableRange)) and (self.currentLongitude <= (self.finalLongitude+acceptableRange)):
            self.longitudeValid=True
        else:
            self.longitudeValid=False
        return self.longitudeValid