# STaTE
# File: EPS.py 
# Purpose: Define EPS subsytem for use in a SimObject thread

import random
import time

class EPS():
    
    ################### INITIALIZE EPS SUBSYTEM #######################
    def __init__(self):
        super().__init__()
        self.checks = {
            'Uplink' : bool(random.getrandbits(1)),
            'Bus Connection' : bool(random.getrandbits(1)),
            'Articulation Gear' : bool(random.getrandbits(1))
        }

        self.distribution = {
            "ACS": 16,
            "EPS": 16,
            "TCS": 16,
            "COMMS": 16,
            "Payload": 16
        }

        self.checkTries = 1
        self.totalPower = 80
        self.statusGood = False
        self.atFullPower = False
        self.solarPanelAngleRange = [-10, 10]
        self.solarPanelAngle = random.randint(-90, 90)
        self.solarPanelAngleGood = False
        self.solarPanelOffBy = 0

        self.telemetryTransferring = False
        self.telemetryTransferComplete = False
        
        # Console infastructure
        self.menu = 'tl'
        self.consoleLog = []
        self.commands = [
            "WELCOME TO THE ELECTRICAL POWER SYSTEMS (EPS) CONSOLE!",
            "Your task is to command the satellite to full power before the payload can be operated.",
            "Enter the command number in the console on the right to execute",
            "1.) Status Checks",
            "2.) Verify Power Distribution System",
            "3.) Full Power",
            "4.) Articulate Panel",
            "5.) Transfer Telemetry"
        ]
    
    ################### EPS CONSOLE COMMANDS #######################
    def command(self, command):
        self.consoleLog.append("$ " + command)
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Power Systems...")
                time.sleep(3)
                self.consoleLog.extend(self.systemChecks())
            elif command_split[0] == "2":
                self.consoleLog.append("Verifying Power Distribution...")
                time.sleep(3)
                self.consoleLog.extend(self.verifyPowerDistribution())
            elif command_split[0] == "3":
                self.consoleLog.append("Redistributing Resources...")
                time.sleep(3)
                self.consoleLog.append(self.fullPower())
            elif command_split[0] == "4":
                self.consoleLog.append("How much do you want to articulate the solar panels by (in Degrees)?")
                self.menu = "panelArticulate"
            elif command_split[0] == "5":
                self.consoleLog.append("Transferring EPS Telemetry...")
                self.consoleLog.append( self.transferTelemetry())
            else:
                self.consoleLog.append("Invalid Command " + command)
        
        elif self.menu == "panelArticulate":
            self.consoleLog.append(self.articulatePanel(int(command)))
            self.menu = "tl"

        elif self.menu == "done":
            self.consoleLog.append("EPS subsystem complete, console closed for commands")

        else:
            self.menu = "tl"

        return self.consoleLog
    
    # tl menu option 1
    def systemChecks(self):
        output = []
        for key in self.checks:
            if (self.checkTries < 2):
                self.checks[key] = bool(random.getrandbits(1))
            else:
                self.checks[key] = True

            if self.checks[key]:
                output.append("..." + str(key) + " Status -- REACHED")
                self.statusGood = True
            else:
                output.append("..." + str(key) + " Status -- NOT REACHED")
                self.statusGood = False

        if self.checkTries > 2:
            self.checkTries = 0
        else:
            self.checkTries += 1
        self.checkPanelAngle()

        if self.solarPanelAngleGood:
            output.append("...Solar Panel Angle -- IN RANGE")
        else:
            output.append("...Solar Panel Angle -- OUT OF RANGE -- OFF BY " + str(self.solarPanelOffBy) + ". Run Articulate Angle to change.")

        return output

    # tl menu option 2
    def verifyPowerDistribution(self):
        output = []
        for key in self.distribution:
            output.append("..." + str(key) + " -- " + str(self.distribution[key]) + "% power")
        output.append("Current power level is at " + str(self.getCurrentTotalPower()) + "%. 100% power is needed for mission completion.")
        return output
    
    def getCurrentTotalPower(self):
        currentPower = 0
        for key in self.distribution:
            currentPower += self.distribution[key]
        return currentPower

    # tl menu option 3
    def fullPower(self):
        self.distribution["ACS"] = 26
        self.distribution["COMMS"] = 26
        self.totalPower = 100
        self.atFullPower = True
        return "System running at full power. Run Verify Power Distribution to verify."

    # tl menu option 4
    def articulatePanel(self, newAngle):
        self.solarPanelAngle += newAngle
        return "Solar panel angle updated by " + str(newAngle)
    
    def checkPanelAngle(self):
        if (self.solarPanelAngle < self.solarPanelAngleRange[0] or self.solarPanelAngle > self.solarPanelAngleRange[1]):
            if (self.solarPanelAngle < self.solarPanelAngleRange[0]):
                self.solarPanelOffBy = self.solarPanelAngle - self.solarPanelAngleRange[0]
            else:
                self.solarPanelOffBy = self.solarPanelAngle - self.solarPanelAngleRange[1]
            self.solarPanelAngleGood = False
        else:
            self.solarPanelAngleGood = True

    # tl menu option 5
    def transferTelemetry(self):
        if self.statusGood and self.solarPanelAngleGood and self.atFullPower:
            self.telemetryTransferring = True
            self.consoleLog.append("Please wait...")
            time.sleep(3)
            self.telemetryTransferring = False
            self.telemetryTransferComplete = True
            self.menu = "done"
            return "Telemetry transfer complete. EPS subsystem complete!"
        else:
            self.telemetryTransferComplete = False
            return "Telemetry cannot be transfered"

    ################### EPS UPDATE #######################
    def update(self):
        self.solarPanelAngle += random.randint(-1,1)