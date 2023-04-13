from simulation.Subsystem import Subsystem
import random

class EPS(Subsystem):
    
    checks = {
        'Uplink' : random.choice([True, False]),
        'Bus Connection' : random.choice([True, False]),
        'Articulation Gear' : random.choice([True, False])
    }

    distribution = {
        "ACS": 16,
        "EPS": 16,
        "TCS": 16,
        "COMMS": 16,
        "Payload": 16
    }

    totalPower = 80
    
    statusGood = False

    telemetryTransferComplete = False
    atFullPower = False

    solarPanelAngleRange = [-10, 10]
    solarPanelAngle = random.randint(-90, 90)
    solarPanelAngleGood = False

    # Console infastructure
    menu = ''
    consoleLog = []
    commands = [
        "WELCOME TO THE ELECTRICAL POWER SYSTEMS (EPS) CONSOLE!",
        "Your task is to command the satellite to full power before the payload can be operated.",
        "1.) Status Checks",
        "2.) Verify Power Distribution System",
        "3.) Full Power",
        "4.) Articulate Panel",
        "5.) Transfer Telemetry"
    ]
    
    def __init__(self):
        super().__init__()
        self.menu = 'tl'
        print("New instance of EPS class created")
        
    def command(self, command):
        
        self.consoleLog.append("$ " + command)
        
        consoleResponse = []
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                consoleResponse.append("Checking Power Systems...")
                consoleResponse.extend(self.systemChecks())
            elif command_split[0] == "2":
                consoleResponse.append("Verifying Power Distribution...")
                consoleResponse.extend(self.verifyPowerDistribution())
            elif command_split[0] == "3":
                consoleResponse.append("Redistributing Resources...")
                consoleResponse.append(self.fullPower())
            elif command_split[0] == "4":
                consoleResponse.append("How much do you want to articulate the solar panels by (in Degrees)?")
                self.menu = "panelArticulate"
            elif command_split[0] == "5":
                consoleResponse.append("Transfering EPS Telemetry...")
                consoleResponse.append( self.transferTelemetry())
                consoleResponse.append("GREAT WORK ON THE ELECTRICAL POWER SYSTEMS (EPS) CONSOLE!")
                #TODO: create instance where user cannot enter commands after subsys finished
            else:
                consoleResponse.append("Invalid Command " + command)
        
        elif self.menu == "panelArticulate":
            consoleResponse.append(self.articulatePanel(int(command)))
            self.menu = "tl"

        else:
            self.menu = "tl"
            
        self.consoleLog.extend(consoleResponse)
        return self.consoleLog
    
    # Main menu option 1
    def systemChecks(self):
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
    def verifyPowerDistribution(self):
        output = []
        index = 0
        for key in self.distribution:
            output[index] = "" + str(key) + " at %" + str(self.distribution[key]) + " power"
            index += 1
        output[index] = "Current power level is at %" + str(self.getCurrentTotalPower()) + ". 100% power is needed for mission completion."
        return output
    
    def getCurrentTotalPower(self):
        currentPower = 0
        for key in self.distribution:
            currentPower += self.distribution[key]
        return currentPower

    # Main menu option 3
    def fullPower(self):
        self.distribution["ACS"] = 26
        self.distribution["COMMS"] = 26
        self.atFullPower = True
        return "System running at full power. Run Verify Power Distribution to verify."

    # Main menu option 4
    def articulatePanel(self, newAngle):
        self.solarPanelAngle += newAngle
        return "Solar panel angle updated by " + str(newAngle)
    
    def checkPanelAngle(self):
        if (self.solarPanelAngle < self.solarPanelAngleRange[0] or self.solarPanelAngle > self.solarPanelAngleRange[1]):
            self.solarPanelAngleGood = False
        else:
            self.solarPanelAngleGood = True

    # Main menu option 5
    def transferTelemetry(self):
        if self.statusGood and self.solarPanelAngleGood and self.atFullPower:
            self.telemetryTransferComplete = True
            return "Telemetry transfer complete. EPS subsystem complete!"
        else:
            self.telemetryTransferComplete = False
            return "Telemetry cannot be transfered"
        
    def update(self):
        self.solarPanelAngle += random.randint(-1,1)
        

    