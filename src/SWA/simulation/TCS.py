import random
import time

class TCS():

    ACSThermal = {
        "CMG": random.randrange(-50,50),
        "Alignment System": random.randrange(-50,50)
    }
    ACSThermalRange = {
        "CMG": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Alignment System": [random.randrange(-100,-20), random.randrange(20, 100)]
    }

    EPSThermal = {
        "Power Distribution": random.randrange(-50,50),
        "Battery": random.randrange(-50,50),
        "Articulation System": random.randrange(-50,50)
    }
    EPSThermalRange = {
        "Power Distribution": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Battery": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Articulation System": [random.randrange(-100,-20), random.randrange(20, 100)]
    }

    COMMSThermal = {
        "On-board Computer": random.randrange(-50,50),
        "Signal Processor": random.randrange(-50,50)
    }
    COMMSThermalRange = {
        "On-board Computer": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Signal Processor": [random.randrange(-100,-20), random.randrange(20, 100)]
    }

    PayloadThermal = {
        "Optical Electronics": random.randrange(-50,50),
        "Gimbal System": random.randrange(-50,50),
        "Imager": random.randrange(-50,50),
    }
    PayloadThermalRange = {
        "Optical Electronics": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Gimbal System": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Imager": [random.randrange(-100,-20), random.randrange(20, 100)]
    }

    SubsystemThermal = {
        "ACS": ACSThermal,
        "EPS": EPSThermal,
        "COMMS": COMMSThermal,
        "Payload": PayloadThermal
    }
    SubsystemThermalRange = {
        "ACS": ACSThermalRange,
        "EPS": EPSThermalRange,
        "COMMS": COMMSThermalRange,
        "Payload": PayloadThermalRange
    }

    checks = {
        'Heating Elements' : random.choice([True, False]),
        'Bus Connection' : random.choice([True, False]),
        'Telemetry Signal' : random.choice([True, False])
    }
    
    checkTries = 0
    telemtryTransferComplete = False

    # Console infastructure
    menu = ''
    consoleLog = []
    commands = [
        "WELCOME TO THE THERMAL CONTROL SYSTEMS (TCS) CONSOLE!",
        "Your task is to perform the cooling procedure for equipment now undergoing thermal exposure in the new attitude position.",
        "1.) Status Check",
        "2.) Verify Thermal Ranges",
        "3.) Cool Subsystems",
        "4.) Transfer Telemetry",
        "5.) Refresh"
    ]

    def __init__(self):
        super().__init__()
        self.menu = 'tl'
        print('New instance of TCS class created')
        
    def command(self, command):
        
        self.consoleLog.append("$ " + command)
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Thermal Systems...")
                time.sleep(5)
                self.consoleLog.extend(self.checkThermalSystems())
            elif command_split[0] == "2":
                self.consoleLog.extend(["Which Subsystem do you want to verify?",
                                        "1) ACS",
                                        "2) EPS",
                                        "3) Payload",
                                        "4) Comms",])
                self.menu = "verifySubsys"
            elif command_split[0] == "3":
                self.consoleLog.extend(["Which Subsystem do you want to cool?",
                                        "1) ACS",
                                        "2) EPS",
                                        "3) Payload",
                                        "4) Comms",])
                self.menu = "coolSubsys"
            elif command_split[0] == "4":
                self.consoleLog.append("Transferring TCS Telemetry...")
                time.sleep(5)
                self.consoleLog.append( self.telemtryTransfer())
                self.consoleLog.append("GREAT WORK ON THE THERMAL CONTROL SYSTEMS (TCS) CONSOLE!")
                #TODO: create instance where user cannot enter commands after subsys finished
            elif command_split[0] == "5":
                #TODO
                pass
            else:
                self.consoleLog.append("Invalid Command " + command)
        
        elif self.menu == "verifySubsys":
            if command_split[0] == "1":
                self.verifySubsystem("ACS")
            elif command_split[0] == "2":
                self.verifySubsystem("EPS")
            elif command_split[0] == "3":
                self.verifySubsystem("Payload")
            elif command_split[0] == "4":
                self.verifySubsystem("COMMS")
            else:
                self.consoleLog.append("Invalid Command " + command)
                self.menu = "tl"
                
        elif self.menu == "verifySubsys":
            if command_split[0] == "1":
                self.verifySubsystem("ACS")
            elif command_split[0] == "2":
                self.verifySubsystem("EPS")
            elif command_split[0] == "3":
                self.verifySubsystem("Payload")
            elif command_split[0] == "4":
                self.verifySubsystem("COMMS")
            else:
                self.consoleLog.append("Invalid Command " + command)
                self.menu = "tl"

        else:
            self.menu = "tl"
            
        return self.consoleLog

    # Heats each item by 1 degree (since you can only cool)
    def randomThermal(self):
        for subsys in self.SubsystemThermal:
            for item in self.SubsystemThermal[subsys]:
                self.SubsystemThermal[subsys][item] += 1

    def update(self):
        self.randomThermal

    ###################TCS CONSOLE COMMANDS #######################
    # Main menu option 1
    def checkThermalSystems(self):
        outputString = []
        for key in self.checks:
            if (self.checkTries < 3):
                self.checks[key] = random.choices([True, False])
                self.checkTries += 1
            else:
                self.checks[key] = True
            if self.checks[key]:
                outputString.append(key + " -- REACHED")
            else:
                outputString.append(key + " -- NOT REACHED, REFRESH SYSTEM")
        if (self.checkTries >= 3):
            self.checkTries = 0
        return outputString    

    # Main menu option 2 with sub-menu option as subsystem string
    # subsystem must be: "ACS", "EPS", "COMMS", or "Payload"            
    def verifySubsystem(self, subsystem):
        output = []
        index = 0
        for item in self.SubsystemThermalRange[subsystem]:
            lower = self.SubsystemThermalRange[subsystem][item][0]
            upper = self.SubsystemThermalRange[subsystem][item][1]
            current = self.SubsystemThermal[subsystem][item]
            output[index] = item + " current temp = " + current + ". Good range: [" + lower + ", " + upper + "]"
            index += 1
        return output
    
    ############# COOLING ###################
    # Main menu option 3
    # subsystem must be: "ACS", "EPS", "COMMS", or "Payload"
    # item must be exactly as string in dictionaries above
    # amount can be positive or negative number
    def coolSubsystemItem(self, subsystem, item, amount):
        self.SubsystemThermal[subsystem][item] += amount

    # Main menu option 4 - telemtry transfer
    def telemtryTransfer(self):
        if self.allSubsystemsInRange:
            self.telemtryTransferComplete = True
            return True
        else:
            return False
    def telemtryTransfer(self):
        if self.verifyStatus:
            return("Data has been Transferred! GREAT WORK ON THE ELECTRICAL POWER SYSTEMS (EPS) CONSOLE")
        else:
            return("Verification process for EPS not completed")
    
    # Main menu option 5 - refresh thermal systems
    def refresh(self):
        for key in self.checks:
            self.checks[key] = True
    
    # Used to check for telemtry transfer
    def allSubsystemsInRange(self):
        for subsys in self.SubsystemThermal:
            for item in self.SubsystemThermal[subsys]:
                lowerRange = self.SubsystemThermalRange[subsys][item][0]
                upperRange = self.SubsystemThermalRange[subsys][item][1]
                itemValue = self.SubsystemThermal[subsys][item]
                if itemValue < lowerRange or itemValue > upperRange:
                    return False
        return True
   
    