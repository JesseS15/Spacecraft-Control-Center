import random
import time

class Payload():

    checks = {
        'Optical Electronics' : random.choice([True, False]),
        'Bus Connection' : random.choice([True, False]),
        'Gimble Connection' : random.choice([True, False])
    }

    checkTries = 0
    ready = False
    statusGood = False
    slewImageFlag = False
    acquireTargetFlag = False
    captureImageFlag = False
    telemetryTransfering = False
    telemetryTransferComplete = False

    # Console infastructure
    menu = ''
    consoleLog = []
    commands = [
        "WELCOME TO THE PAYLOAD (PL) CONSOLE!",
        "Your task is to capture imagery of the target during the flyover period.",
        "Enter the command number in the console on the right to execute",
        "1.) Status Checks",
        "2.) Slew Image",
        "3.) Acquire Target",
        "4.) Capture Image",
        "5.) Transfer Telemetry"
    ]

    def __init__(self):
        self.menu = 'tl'
        super().__init__()
        
    def command(self, command):
        
        self.consoleLog.append("$ " + command)
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Power Systems...")
                time.sleep(5)
                self.consoleLog.extend(self.statusChecks())
            elif command_split[0] == "2":
                self.consoleLog.append("Slew Commencing...")
                time.sleep(5)
                self.consoleLog.append(self.slewImage())
            elif command_split[0] == "3":
                self.consoleLog.append("Acquiring Target...")
                time.sleep(5)
                self.consoleLog.append(self.acquireTarget())
            elif command_split[0] == "4":
                self.consoleLog.append("Capturing Image...")
                time.sleep(5)
                self.consoleLog.append(self.captureImage())
            elif command_split[0] == "5":
                self.consoleLog.append("Transferring Payload Telemetry...")
                self.consoleLog.append( self.telemetryTransfer())
                self.consoleLog.append("GREAT WORK ON THE PAYLOAD SYSTEM CONSOLE!")
            else:
                self.consoleLog.append("Invalid Command " + command)

        elif self.menu == "done":
            self.consoleLog.append("Payload subsystem complete, console closed for commands")
                
        else:
            self.menu = "tl"
            
        return self.consoleLog

    # Main menu option 1
    def statusChecks(self):
        output = []
        index = 0
        self.statusGood = True
        for key in self.checks:
            if (self.checkTries < 3):
                self.checks[key] = random.choices([True, False])
                self.checkTries += 1
            else:
                self.checks[key] = True
            if self.checks[key]:
                output[index] = "The SimCrafts current " + key + " Status is REACHED"
            else:
                output[index] = "The SimCrafts current " + key + " Status is NOT REACHED"
                self.statusGood = False
            index += 1

        if (self.checkTries >= 3):
            self.checkTries = 0
        return output

    # Main menu option 2
    def slewImage(self):
        if self.statusGood and self.ready:
            self.slewImageFlag = True
            return "The imager has reached the ground target!"
        else:
            return "The imager has not reached the ground target."

    # Main menu option 3
    def acquireTarget(self):
        if self.slewImageFlag:
            self.acquireTargetFlag = True
            return "The ground target has been acquired successfully!"
        else:
            return "The ground target cannot be acquired at this time."

    # Main menu option 4
    def captureImage(self):
        if self.acquireTargetFlag:
            self.captureImageFlag = True
            return "The ground image has been captured successfully!"
        else:
            return "The ground image cannot be captured at this time."

    # Main menu option 5
    def telemetryTransfer(self):
        if self.captureImageFlag:
            self.telemetryTransfering = True
            time.sleep(5)
            self.telemetryTransfering = False
            self.telemetryTransferComplete = True
            self.menu = "done"
            return True
        else:
            return False



