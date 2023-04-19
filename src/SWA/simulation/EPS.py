import random
import time

class EPS():
    
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

    checkTries = 0
    totalPower = 80
    statusGood = False
    atFullPower = False
    solarPanelAngleRange = [-10, 10]
    solarPanelAngle = random.randint(-90, 90)
    solarPanelAngleGood = False

    telemetryTransfering = False
    telemetryTransferComplete = False
    
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
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Power Systems...")
                time.sleep(5)
                self.consoleLog.extend(self.systemChecks())
            elif command_split[0] == "2":
                self.consoleLog.append("Verifying Power Distribution...")
                time.sleep(5)
                self.consoleLog.extend(self.verifyPowerDistribution())
            elif command_split[0] == "3":
                self.consoleLog.append("Redistributing Resources...")
                time.sleep(5)
                self.consoleLog.append(self.fullPower())
            elif command_split[0] == "4":
                self.consoleLog.append("How much do you want to articulate the solar panels by (in Degrees)?")
                self.menu = "panelArticulate"
            elif command_split[0] == "5":
                self.consoleLog.append("Transfering EPS Telemetry...")
                self.consoleLog.append( self.transferTelemetry())
                self.consoleLog.append("GREAT WORK ON THE ELECTRICAL POWER SYSTEMS (EPS) CONSOLE!")
                #TODO: create instance where user cannot enter commands after subsys finished
            else:
                self.consoleLog.append("Invalid Command " + command)
        
        elif self.menu == "panelArticulate":
            self.consoleLog.append(self.articulatePanel(int(command)))
            self.menu = "tl"

        else:
            self.menu = "tl"
        
        return self.consoleLog
    
    # Main menu option 1
    def systemChecks(self):
        output = []
        index = 0
        for key in self.checks:
            if (self.checkTries < 3):
                self.checks[key] = random.choices([True, False])
                self.checkTries += 1
            else:
                self.checks[key] = True
            if self.checks[key]:
                output[index] = "--The SimCrafts current " + str(key) + " Status is REACHED"
                self.statusGood = True
            else:
                output[index] = "--The SimCrafts current " + str(key) + " Status is NOT REACHED"
                self.statusGood = False
            index += 1

        if (self.checkTries >= 3):
            self.checkTries = 0
        return output

    # Main menu option 2
    def verifyPowerDistribution(self):
        output = []
        index = 0
        for key in self.distribution:
            output[index] = "--" + str(key) + " at %" + str(self.distribution[key]) + " power"
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
        self.totalPower = 100
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
            self.telemetryTransfering = True
            time.sleep(5)
            self.telemetryTransfering = False
            self.telemetryTransferComplete = True
            return "Telemetry transfer complete. EPS subsystem complete!"
        else:
            self.telemetryTransferComplete = False
            return "Telemetry cannot be transfered"
        
    def update(self):
        self.solarPanelAngle += random.randint(-1,1)
        

    