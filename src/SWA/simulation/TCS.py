# STaTE
# File: TCS.py 
# Purpose: Define TCS subsytem for use in a SimObject thread

import random
import time

class TCS():

    ################### INITIALIZE TCS SUBSYTEM #######################
    def __init__(self):
        super().__init__()
        
        self.ACSThermal = {
            "CMG": random.randrange(-50,50),
            "Alignment System": random.randrange(-50,50)
        }
        self.ACSThermalRange = {
            "CMG": [random.randrange(-100,-20), random.randrange(20, 100)],
            "Alignment System": [random.randrange(-100,-20), random.randrange(20, 100)]
        }

        self.EPSThermal = {
            "Power Distribution": random.randrange(-50,50),
            "Battery": random.randrange(-50,50),
            "Articulation System": random.randrange(-50,50)
        }
        self.EPSThermalRange = {
            "Power Distribution": [random.randrange(-100,-20), random.randrange(20, 100)],
            "Battery": [random.randrange(-100,-20), random.randrange(20, 100)],
            "Articulation System": [random.randrange(-100,-20), random.randrange(20, 100)]
        }

        self.COMMSThermal = {
            "On-board Computer": random.randrange(-50,50),
            "Signal Processor": random.randrange(-50,50)
        }
        self.COMMSThermalRange = {
            "On-board Computer": [random.randrange(-100,-20), random.randrange(20, 100)],
            "Signal Processor": [random.randrange(-100,-20), random.randrange(20, 100)]
        }

        self.PayloadThermal = {
            "Optical Electronics": random.randrange(-50,50),
            "Gimbal System": random.randrange(-50,50),
            "Imager": random.randrange(-50,50),
        }
        self.PayloadThermalRange = {
            "Optical Electronics": [random.randrange(-100,-20), random.randrange(20, 100)],
            "Gimbal System": [random.randrange(-100,-20), random.randrange(20, 100)],
            "Imager": [random.randrange(-100,-20), random.randrange(20, 100)]
        }

        self.SubsystemThermal = {
            "ACS": self.ACSThermal,
            "EPS": self.EPSThermal,
            "COMMS": self.COMMSThermal,
            "Payload": self.PayloadThermal
        }
        self.SubsystemThermalRange = {
            "ACS": self.ACSThermalRange,
            "EPS": self.EPSThermalRange,
            "COMMS": self.COMMSThermalRange,
            "Payload": self.PayloadThermalRange
        }

        self.checks = {
            'Heating Elements' : bool(random.getrandbits(1)),
            'Bus Connection' : bool(random.getrandbits(1)),
            'Telemetry Signal' : bool(random.getrandbits(1))
        }

        # Needed to make sure random functions dont return the same value everytime
        random.seed()
        
        self.checkTries = 0
        self.checksGood = False
        
        self.telemetryTransferring = False
        self.telemetryTransferComplete = False

        # Console infastructure
        self.menu = 'tl'
        self.consoleLog = []
        self.commands = [
            "WELCOME TO THE THERMAL CONTROL SYSTEMS (TCS) CONSOLE!",
            "Your task is to perform the cooling procedure for equipment now undergoing thermal exposure in the new attitude position.",
            "Enter the command number in the console on the right to execute",
            "1.) Status Check",
            "2.) Verify Thermal Ranges",
            "3.) Cool Subsystems",
            "4.) Transfer Telemetry",
            "5.) Refresh"
        ]

    ################### TCS CONSOLE COMMANDS #######################
    def command(self, command):
        self.consoleLog.append("$ " + command)
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Thermal Systems...")
                time.sleep(3)
                self.consoleLog.extend(self.checkThermalSystems())
            elif command_split[0] == "2":
                self.consoleLog.append("Verifying subsystems...")
                time.sleep(1)
                self.consoleLog.extend(self.verifySubsystem())
            elif command_split[0] == "3":
                self.consoleLog.extend(["Which Subsystem do you want to cool?",
                                        "1) ACS",
                                        "2) EPS",
                                        "3) Comms",
                                        "4) Payload",])
                self.menu = "coolSubsys"
            elif command_split[0] == "4":
                self.consoleLog.append("Transferring TCS Telemetry...")
                self.consoleLog.extend(self.telemetryTransfer())
            elif command_split[0] == "5":
                self.consoleLog.append(self.refresh())
            else:
                self.consoleLog.append("Invalid Command " + command)

        elif self.menu == "coolSubsys":
            if command_split[0] == "1":
                self.consoleLog.extend(["Which ACS item would you like to cool?",
                                        "1) CMG",
                                        "2) Alignment System"])
                self.menu = "acsCool"
            elif command_split[0] == "2":
                self.consoleLog.extend(["Which EPS item would you like to cool?",
                                        "1) Power Distribution",
                                        "2) Battery",
                                        "3) Articulation System"])
                self.menu = "epsCool"
            elif command_split[0] == "3":
                self.consoleLog.extend(["Which COMMS item would you like to cool?",
                                        "1) On-board Computer",
                                        "2) Signal Processor"])
                self.menu = "commsCool"
            elif command_split[0] == "4":
                self.consoleLog.extend(["Which Payload item would you like to cool?",
                                        "1) Optical Electronics",
                                        "2) Gimbal System",
                                        "3) Imager"])
                self.menu = "payloadCool"
            else:
                self.consoleLog.append("Invalid Command " + command)
                self.menu = "tl"

        elif self.menu == "acsCool":
            if command_split[0] == "1":
                self.consoleLog.append("How much would you like to cool the ACS CMG by?")
                self.coolChange = ["ACS", "CMG"]
                self.menu = "cool"
            elif command_split[0] == "2":
                self.consoleLog.append("How much would you like to cool the ACS Alignment System by?")
                self.coolChange = ["ACS", "Alignment System"]
                self.menu = "cool"
            else:
                self.consoleLog.append("Invalid Command " + command)
                self.menu = "tl"

        elif self.menu == "epsCool":
            if command_split[0] == "1":
                self.consoleLog.append("How much would you like to cool the EPS Power Distribution by?")
                self.coolChange = ["EPS", "Power Distribution"]
                self.menu = "cool"
            elif command_split[0] == "2":
                self.consoleLog.append("How much would you like to cool the EPS Battery by?")
                self.coolChange = ["EPS", "Battery"]
                self.menu = "cool"
            elif command_split[0] == "3":
                self.consoleLog.append("How much would you like to cool the EPS Articulation System by?")
                self.coolChange = ["EPS", "Articulation System"]
                self.menu = "cool"
            else:
                self.consoleLog.append("Invalid Command " + command)
                self.menu = "tl"

        elif self.menu == "payloadCool":
            if command_split[0] == "1":
                self.consoleLog.append("How much would you like to cool the Payload Optical Electronics by?")
                self.coolChange = ["Payload", "Optical Electronics"]
                self.menu = "cool"
            elif command_split[0] == "2":
                self.consoleLog.append("How much would you like to cool the Payload Signal Processor by?")
                self.coolChange = ["Payload", "Gimbal System"]
                self.menu = "cool"
            elif command_split[0] == "3":
                self.consoleLog.append("How much would you like to cool the Payload Imager by?")
                self.coolChange = ["Payload", "Imager"]
                self.menu = "cool"
            else:
                self.consoleLog.append("Invalid Command " + command)
                self.menu = "tl"

        elif self.menu == "commsCool":
            if command_split[0] == "1":
                self.consoleLog.append("How much would you like to cool the COMMS On-board Computer by?")
                self.coolChange = ["COMMS", "On-board Computer"]
                self.menu = "cool"
            elif command_split[0] == "2":
                self.consoleLog.append("How much would you like to cool the Payload Signal Processor by?")
                self.coolChange = ["COMMS", "Signal Processor"]
                self.menu = "cool"
            else:
                self.consoleLog.append("Invalid Command " + command)
                self.menu = "tl"

        elif self.menu == "cool":
            self.consoleLog.append(self.coolSubsystemItem(self.coolChange[0], self.coolChange[1], int(command)))
            self.menu = "tl"

        elif self.menu == "done":
            self.consoleLog.append("TCS subsystem completed, console closed for commands")

        else:
            self.menu = "tl"
            
        return self.consoleLog
    
    # tl menu option 1
    def checkThermalSystems(self):
        outputString = []
        self.checksGood = True
        for key in self.checks:
            if self.checkTries < 2:
                self.checks[key] = bool(random.getrandbits(1))
            else:
                self.checks[key] = True
                
            if self.checks[key]:
                outputString.append(key + " -- REACHED")
            else:
                outputString.append(key + " -- NOT REACHED, REFRESH SYSTEM")
                self.checksGood = False
        if self.checkTries > 2:
            self.checkTries = 0
        else:
            self.checkTries += 1
        return outputString    

    # tl menu option 2 with sub-menu option as subsystem string
    # subsystem must be: "ACS", "EPS", "COMMS", or "Payload"            
    def verifySubsystem(self):
        output = []
        for subsystem in self.SubsystemThermalRange:
            output.append(subsystem + " Ranges:")
            for item in self.SubsystemThermalRange[subsystem]:
                lower = self.SubsystemThermalRange[subsystem][item][0]
                upper = self.SubsystemThermalRange[subsystem][item][1]
                current = self.SubsystemThermal[subsystem][item]
                if self.subsystemItemInRange(subsystem, item):
                    output.append("- " + str(item) + " current temp = " + str(current) + " -- IN RANGE")
                else:
                    output.append("- " + str(item) + " current temp = " + str(current) + " -- OUT OF RANGE -- Good range: [" + str(lower) + ", " + str(upper) + "]")
        return output
    
    def subsystemItemInRange(self, subsystem, item):
        lowerRange = self.SubsystemThermalRange[subsystem][item][0]
        upperRange = self.SubsystemThermalRange[subsystem][item][1]
        itemValue = self.SubsystemThermal[subsystem][item]
        if itemValue < lowerRange or itemValue > upperRange:
            return False
        else:
            return True
    
    # tl menu option 3 - Cool subsytem
    # subsystem must be: "ACS", "EPS", "COMMS", or "Payload"
    # item must be exactly as string in dictionaries above
    # amount can be positive or negative number
    def coolSubsystemItem(self, subsystem, item, amount):
        if (abs(amount) > 500):
            return ("ERROR -- Attempting to cool by too much -- TRY AGAIN")
        else:
            self.SubsystemThermal[subsystem][item] += amount
            return (str(subsystem) + " " + str(item) + " cooled by " + str(amount))

    # tl menu option 4 - telemtry transfer
    def telemetryTransfer(self):
        output = []
        if self.allSubsystemsInRange() and self.checksGood:
            self.telemetryTransferring = True
            self.consoleLog.append("Please wait...")
            time.sleep(5)
            self.telemetryTransferring = False
            self.telemetryTransferComplete = True
            self.menu = "done"
            output.append("Data has been Transferred!")
            output.append("GREAT WORK ON THE THERMAL CONTROL SUBSYSTEM (TCS) CONSOLE")
            return output
        else:
            self.menu = "tl"
            output.append("Verification process for TCS not completed -- Temps not in range")  
            return output       
    
    # tl menu option 5 - refresh thermal systems
    def refresh(self):
        for key in self.checks:
            self.checks[key] = True
        self.checksGood = True
        self.checkTries = 4
        return "Systems refreshed, run System Checks to verify."
    
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
    
    ################### TCS UPDATE #######################
    # Heats each item by 1 degree every 5 seconds (since you can only cool)
    def update(self):
        time.sleep(5)
        if not self.telemetryTransferComplete:
            for subsys in self.SubsystemThermal:
                for item in self.SubsystemThermal[subsys]:
                    self.SubsystemThermal[subsys][item] += 1