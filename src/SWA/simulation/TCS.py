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
        'Heating Elements' : bool(random.getrandbits(1)),
        'Bus Connection' : bool(random.getrandbits(1)),
        'Telemetry Signal' : bool(random.getrandbits(1))
    }

    # Needed to make sure random functions dont return the same value everytime
    random.seed()
    
    checkTries = 0
    checksGood = False
    
    telemetryTransfering = False
    telemetryTransferComplete = False

    # Console infastructure
    menu = ''
    consoleLog = []
    commands = [
        "WELCOME TO THE THERMAL CONTROL SYSTEMS (TCS) CONSOLE!",
        "Your task is to perform the cooling procedure for equipment now undergoing thermal exposure in the new attitude position.",
        "Enter the command number in the console on the right to execute",
        "1.) Status Check",
        "2.) Verify Thermal Ranges",
        "3.) Cool Subsystems",
        "4.) Transfer Telemetry",
        "5.) Refresh"
    ]

    def __init__(self):
        super().__init__()
        self.menu = 'tl'
        self.checkTries = 0
        print('New instance of TCS class created')
        
    def command(self, command):
        
        self.consoleLog.append("$ " + command)
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Thermal Systems...")
                time.sleep(2)
                self.consoleLog.extend(self.checkThermalSystems())
            elif command_split[0] == "2":
                self.consoleLog.append("Verifying subsystems...")
                time.sleep(2)
                self.consoleLog.extend(self.verifySubsystem())
            elif command_split[0] == "3":
                self.consoleLog.extend(["Which Subsystem do you want to cool?",
                                        "1) ACS",
                                        "2) EPS",
                                        "3) Payload",
                                        "4) Comms",])
                self.menu = "coolSubsys"
            elif command_split[0] == "4":
                self.consoleLog.append("Transferring TCS Telemetry...")
                self.consoleLog.append(self.telemetryTransfer())
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
                self.consoleLog.extend(["Which Payload item would you like to cool?",
                                        "1) Optical Electronics",
                                        "2) Gimbal System",
                                        "3) Imager"])
                self.menu = "payloadCool"
            elif command_split[0] == "4":
                self.consoleLog.extend(["Which COMMS item would you like to cool?",
                                        "1) On-board Computer",
                                        "2) Signal Processor"])
                self.menu = "commsCool"
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
                self.consoleLog.append(self.coolSubsystemItem("COMMS", "Signal Processor", int(command)))
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

    # Heats each item by 1 degree (since you can only cool)
    def update(self):
        if not self.telemetryTransferComplete:
            for subsys in self.SubsystemThermal:
                for item in self.SubsystemThermal[subsys]:
                    self.SubsystemThermal[subsys][item] += 1

    ###################TCS CONSOLE COMMANDS #######################
    # Main menu option 1
    def checkThermalSystems(self):
        outputString = []
        self.checksGood = True
        for key in self.checks:
            if self.checkTries < 3:
                self.checks[key] = bool(random.getrandbits(1))
                self.checkTries += 1
            if self.checks[key]:
                outputString.append(key + " -- REACHED")
            else:
                outputString.append(key + " -- NOT REACHED, REFRESH SYSTEM")
                self.checksGood = False
        if self.checkTries >= 3:
            self.checkTries = 0
        return outputString    

    # Main menu option 2 with sub-menu option as subsystem string
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
    
    ############# COOLING ###################
    # Main menu option 3
    # subsystem must be: "ACS", "EPS", "COMMS", or "Payload"
    # item must be exactly as string in dictionaries above
    # amount can be positive or negative number
    def coolSubsystemItem(self, subsystem, item, amount):
        self.SubsystemThermal[subsystem][item] += amount
        return (str(subsystem) + " " + str(item) + " cooled by " + str(amount))

    # Main menu option 4 - telemtry transfer
    def telemetryTransfer(self):
        if self.allSubsystemsInRange() and self.checksGood:
            self.telemetryTransfering = True
            self.consoleLog.append("Please wait...")
            time.sleep(5)
            self.telemetryTransfering = False
            self.telemetryTransferComplete = True
            self.menu = "done"
            return ["Data has been Transferred!", "GREAT WORK ON THE THERMAL CONTROL SUBSYSTEM (TCS) CONSOLE"]
        else:
            self.menu = "tl"
            return ("Verification process for TCS not completed -- Temps not in range")          
    
    # Main menu option 5 - refresh thermal systems
    def refresh(self):
        for key in self.checks:
            self.checks[key] = True
        self.checksGood = True
        self.checkTries = 4
        return ("Systems refreshed, run System Checks to verify.")
    
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
   
    