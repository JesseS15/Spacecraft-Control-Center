# STaTE
# File: COMMS.py 
# Purpose: Define COMMS subsytem for use in a SimObject thread

import random
import time

class COMMS():
    
    ################### INITIALIZE COMMS SUBSYTEM #######################
    def __init__(self):
        super().__init__()
        self.checks = {
            "On-board Computer": bool(random.getrandbits(1)),
            "Antenna Status": bool(random.getrandbits(1))
        }

        self.subsystemComplete = False

        self.checkTries = 0

        self.frequency = random.randrange(12.000, 14.000)
        self.currentGain = 36
        self.gainRange = [36,38]

        self.allTelemetryDataGood = False
        self.allTelemetryData = {"ACS": False, "EPS": False, "TCS": False, "Payload": False}

        # Console infastructure
        self.menu = 'tl'
        self.consoleLog = []
        self.commands = [
            "WELCOME TO THE COMMUNICATIONS (COMMS) CONSOLE",
            "Your task is to verify that signal lock is established between the Ku-Band satellite antenna and the ground station antenna, transmit the target image to the ground station, process the image, and display the results.",
            "Enter the command number in the console on the right to execute",
            "1.) Status Checks",
            "2.) Verify Signal",
            "3.) Increase Signal Gain",
            "4.) Reset Signal Gain",
            "5.) Download Telemetry Data",
            "6.) Process Telemetry Data",
            "7.) Display Image"
        ]

    ################### COMMS CONSOLE COMMANDS #######################
    def command(self, command):
        self.consoleLog.append("$ " + command) 
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            
            if command_split[0] == "1":
                self.consoleLog.append("Checking Communication Systems...")
                time.sleep(3)
                self.consoleLog.extend(self.systemChecks())
            elif command_split[0] == "2":
                self.consoleLog.append("Verifying Signal...")
                time.sleep(3)
                self.consoleLog.extend(self.verifySignal())
            elif command_split[0] == "3":
                self.consoleLog.append("How much do you want to increase the Signal Gain (in dB)?")
                self.menu = "signalGainIncrease"
            elif command_split[0] == "4":
                self.consoleLog.extend(self.resetGain())
            elif command_split[0] == "5":
                self.consoleLog.append("Downloading Subsystem Telemetry...")
                time.sleep(3)
                self.consoleLog.extend(self.downloadTelemetryData())
            elif command_split[0] == "6":
                self.consoleLog.append("Processing SimCraft Telemetry...")
                time.sleep(3)
                self.consoleLog.append(self.processTelemetryData())
            elif command_split[0] == "7":
                self.consoleLog.append("Attempting to display image...")
                time.sleep(3)
                self.consoleLog.extend(self.displayImage())
            else:
                self.consoleLog.append("Invalid Command " + command)
        
        elif self.menu == "signalGainIncrease":
            self.consoleLog.extend(self.increaseGain(int(command)))
            self.menu = "tl"

        elif self.menu == "done":
            self.consoleLog.append("Mission Completed, console closed for commands")
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

            if (self.checks[key]):
                output.append("..." + str.capitalize(key) + " -- REACHED")
            else:
                output.append("..." + str.capitalize(key) + " -- NOT REACHED")

        if self.checkTries > 2:
            self.checkTries = 0
        else:
            self.checkTries += 1
        return output

    # tl menu option 2
    def verifySignal(self):
        output = []
        if (self.currentGain >= self.gainRange[0]) and (self.currentGain <= self.gainRange[1]):
            self.checks['Antenna Status'] = True
            output.append('...Signal -- CAPTURED -- Current Gain at ' + str(self.currentGain) + " dB")
        elif self.currentGain > self.gainRange[1]:
            output.append('...Signal -- NOT CAPTURED -- Gain too high! Reset gain')
        else:
            output.append('...Signal -- NOT CAPTURED -- Increase gain to 38 dB')
        return output

    # tl menu option 3    
    def increaseGain(self, newGin):
        output = []
        output.append('...GAIN CHANGING -- Please wait...')
        output.append("Gain changed by " + str(abs(newGin)))
        self.currentGain += abs(newGin)
        return output
    
    # tl menu option 4
    def resetGain(self):
        output = []
        self.currentGain = self.gainRange[0]
        output.append("...GAIN RESETTING -- Please wait...")
        output.append("Gain reset to " + str(self.currentGain) + " dB")
        return output
    
    # tl menu option 5
    def downloadTelemetryData(self):
        output = []
        self.allTelemetryDataGood = True
        for key in self.allTelemetryData:
            if self.allTelemetryData[key]:
                output.append("..." + key + " Telemetry -- COMPLETE!")
            else:
                output.append("..." + key + " Telemetry -- INCOMPLETE!")
                self.allTelemetryDataGood = False
        if (self.allTelemetryDataGood):
            output.append("The Subsystem Telemetry Data has been successfully downloaded!")
        else:
            output.append("Some subsystems have not complete their missions yet and need to send their telemetry data to finish your task.")
        return output

    # tl menu option 6
    def processTelemetryData(self):
        if self.allTelemetryDataGood:
            return "All telemetry data has been successfully processed!"
        else:
            return "Some subsystems have not complete their missions yet and need to send their telemetry data to finish your task."

    # tl menu option 7
    def displayImage(self):
        output = []
        if self.allTelemetryDataGood:
            self.consoleLog.append("All telemetry data has been successfully processed!")
            self.consoleLog.append("GREAT WORK ON THE COMMS SYSTEM CONSOLE")
            self.consoleLog.append("Mission accomplished!")
            self.consoleLog.append("Displaying image...")
            time.sleep(3)
            self.subsystemComplete = True
            self.menu = "done"
        else:
            output.append("Some subsystems have not complete their missions yet and need to send their telemetry data to finish your task.")
        return output
    
    ################### COMMS UPDATE #######################
    def update(self):
        return self.subsystemComplete


