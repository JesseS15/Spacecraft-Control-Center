from simulation.Subsystem import Subsystem
import random

class payload(Subsystem):

    checks = {
        'Optical Electronics' : random.choice([True, False]),
        'Bus Connection' : random.choice([True, False]),
        'Gimble Connection' : random.choice([True, False])
    }

    ready = False
    statusGood = False
    slewImageFlag = False
    acquireTargetFlag = False
    captureImageFlag = False
    telemetryTransferComplete = False

    # Console infastructure
    menu = ''
    consoleLog = []
    commands = [
        "WELCOME TO THE PAYLOAD (PL) CONSOLE!",
        "Your task is to capture imagery of the target during the flyover period.",
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
        
        consoleResponse = []
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                consoleResponse.append("Checking Power Systems...")
                consoleResponse.extend(self.statusChecks())
            elif command_split[0] == "2":
                consoleResponse.append("Slew Commencing...")
                consoleResponse.append(self.slewImage())
            elif command_split[0] == "3":
                consoleResponse.append("Acquiring Target...")
                consoleResponse.append(self.acquireTarget())
            elif command_split[0] == "4":
                consoleResponse.append("Capturing Image...")
                consoleResponse.append(self.captureImage())
            elif command_split[0] == "5":
                consoleResponse.append("Transferring Payload Telemetry...")
                consoleResponse.append( self.telemetryTransfer())
                consoleResponse.append("GREAT WORK ON THE PAYLOAD SYSTEM CONSOLE!")
                #TODO: create instance where user cannot enter commands after subsys finished
            else:
                consoleResponse.append("Invalid Command " + command)
                
        else:
            self.menu = "tl"
            
        self.consoleLog.extend(consoleResponse)
        return self.consoleLog

    # Main menu option 1
    def statusChecks(self):
        output = []
        index = 0
        self.statusGood = True
        for key in self.checks:
            self.checks[key] = random.choice([True, False])
            if self.checks[key]:
                output[index] = "The SimCrafts current " + key + " Status is REACHED"
            else:
                output[index] = "The SimCrafts current " + key + " Status is NOT REACHED"
                self.statusGood = False
            index += 1
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
            self.telemetryTransferComplete = True
            return True
        else:
            return False



