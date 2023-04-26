# STaTE
# File: Payload.py 
# Purpose: Define Payload subsytem for use in a SimObject thread

import random
import time

class Payload():

    ################### INITIALIZE Payload SUBSYTEM #######################
    def __init__(self):
        super().__init__()
        self.checks = {
            'Optical Electronics' : bool(random.getrandbits(1)),
            'Bus Connection' : bool(random.getrandbits(1)),
            'Gimble Connection' : bool(random.getrandbits(1))
        }

        self.checkTries = 0
        self.ready = False
        self.statusGood = False
        self.slewImageFlag = False
        self.acquireTargetFlag = False
        self.captureImageFlag = False
        self.telemetryTransferring = False
        self.telemetryTransferComplete = False
        
        self.gimbalStatus = True
        self.imagerStatus = True

        # Console infastructure
        self.menu = 'tl'
        self.consoleLog = []
        self.commands = [
            "WELCOME TO THE PAYLOAD (PL) CONSOLE!",
            "Your task is to capture imagery of the target during the flyover period.",
            "Enter the command number in the console on the right to execute",
            "1.) Status Checks",
            "2.) Slew Image",
            "3.) Acquire Target",
            "4.) Capture Image",
            "5.) Transfer Telemetry"
        ]
        
    ################### COMMAND Payload SUBSYTEM #######################
    def command(self, command):
        self.consoleLog.append("$ " + command)
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Payload Status...")
                time.sleep(3)
                self.consoleLog.extend(self.statusChecks())
            elif command_split[0] == "2":
                self.consoleLog.append("Slew Commencing...")
                time.sleep(3)
                self.consoleLog.extend(self.slewImage())
            elif command_split[0] == "3":
                self.consoleLog.append("Acquiring Target...")
                time.sleep(3)
                self.consoleLog.extend(self.acquireTarget())
            elif command_split[0] == "4":
                self.consoleLog.append("Capturing Image...")
                time.sleep(3)
                self.consoleLog.extend(self.captureImage())
            elif command_split[0] == "5":
                self.consoleLog.append("Transferring Payload Telemetry...")
                self.consoleLog.extend(self.telemetryTransfer())
            else:
                self.consoleLog.append("Invalid Command " + command)

        elif self.menu == "done":
            self.consoleLog.append("Payload subsystem complete, console closed for commands")
                
        else:
            self.menu = "tl"
            
        return self.consoleLog

    # tl menu option 1
    def statusChecks(self):
        output = []
        self.statusGood = True
        for key in self.checks:
            if (self.checkTries < 2):
                self.checks[key] = bool(random.getrandbits(1))
            else:
                self.checks[key] = True

            if self.checks[key]:
                output.append("..." + key + " -- REACHED")
            else:
                output.append("..." + key + " -- NOT REACHED")
                self.statusGood = False

        if (self.checkTries > 2):
            self.checkTries = 0
        else:
            self.checkTries += 1
        return output

    # tl menu option 2
    def slewImage(self):
        output = []
        if self.statusGood and self.ready:
            self.slewImageFlag = True
            output.append("...Ground Target -- REACHED")
        else:
            if not self.ready:
                output.append("...Ground Target -- NOT REACHED -- Longitude not within range.")
                output.append("Check with ACS to determine ETA.")
            if not self.statusGood:
                output.append("...Ground Target -- NOT REACHED -- Payload Status not reached.")
                output.append("Run status checks to verify ground target has been reached.")
        return output

    # tl menu option 3
    def acquireTarget(self):
        output = []
        if self.slewImageFlag:
            self.acquireTargetFlag = True
            output.append("...Ground Target -- ACQUIRED")
        else:
            output.append("...Ground Target -- CANNOT BE ACQUIRED")
            output.append("Run Slew Image to check if ground target has been reached")
        return output

    # tl menu option 4
    def captureImage(self):
        output = []
        if self.acquireTargetFlag:
            self.captureImageFlag = True
            output.append("...Image -- CAPTURED")
        else:
            output.append("...Image -- NOT CAPTURED")
            output.append("Target has not been acquired")
        return output

    # tl menu option 5
    def telemetryTransfer(self):
        output = []
        if self.captureImageFlag:
            self.telemetryTransferring = True
            self.consoleLog.append("Please wait...")
            time.sleep(3)
            self.telemetryTransferring = False
            self.telemetryTransferComplete = True
            output.append("...Telemetry Transfer -- COMPLETE")
            output.append("GREAT WORK ON THE PAYLOAD SYSTEM CONSOLE!")
            self.menu = "done"
            return output
        else:
            self.menu = "tl"
            output.append("!! Data Transfer Error -- Image has not been captured !!")  
            return output  

    ################### UPDATE Payload SUBSYTEM #######################
    def update(self):
        pass