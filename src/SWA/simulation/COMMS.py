import random
import time

class COMMS():

    checks = {
        "On-board Computer": random.choices([True, False]),
        "Antenna Status": random.choices([True, False])
    }

    checkTries = 0

    frequency = random.randrange(12.000, 14.000)
    currentGain = 36
    gainRange = [36,38]

    allTelemetryDataGood = False
    allTelemetryData = {"ACS": False, "EPS": False, "TCS": False, "Payload": False}

    # Console infastructure
    menu = ''
    consoleLog = []
    commands = [
        "WELCOME TO THE COMMUNICATIONS (COMMS) CONSOLE",
        "Your task is to verify that signal lock is established between the Ku-Band satellite antenna and the ground station antenna, transmit the target image to the ground station, process the image, and display the results.",
        "1.) Status Checks",
        "2.) Verify Signal",
        "3.) Increase Signal Gain",
        "4.) Reset Signal Gain",
        "5.) Download Telemetry Data",
        "6.) Process Telemetry Data",
        "7.) Display Image"
    ]
    
    def __init__(self):
        super().__init__()
        self.menu = 'tl'
        print('New instance of COMMS class created')

    def command(self, command):
        
        self.consoleLog.append("$ " + command)
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                self.consoleLog.append("Checking Communication Systems...")
                time.sleep(5)
                self.consoleLog.extend(self.systemChecks())
            elif command_split[0] == "2":
                self.consoleLog.append("Verifying Signal...")
                time.sleep(5)
                self.consoleLog.append(self.verifySignal())
            elif command_split[0] == "3":
                self.consoleLog.append("How much do you want to increase the Signal Gain (in dB)?")
                self.menu = "signalGainIncrease"
            elif command_split[0] == "4":
                self.consoleLog.append("Resetting gain to 36 dB")
                self.consoleLog.extend(self.resetGain())
            elif command_split[0] == "5":
                self.consoleLog.append("Downloading Subsystem Telemetry...")
                time.sleep(5)
                self.consoleLog.extend(self.downloadTelemetryData())
            elif command_split[0] == "6":
                self.consoleLog.append("Processing SimCraft Telemetry...")
                time.sleep(5)
                self.consoleLog.append(self.processTelemetryData())
            elif command_split[0] == "7":
                self.consoleLog.append("Attempting to displaying Image...")
                time.sleep(5)
                self.consoleLog.extend(self.displayImage())
                #TODO: create instance where user cannot enter commands after subsys finished
            else:
                self.consoleLog.append("Invalid Command " + command)
        
        elif self.menu == "signalGainIncrease":
            self.consoleLog.extend(self.increaseGain(int(command)))
            self.menu = "tl"
        else:
            self.menu = "tl"
        
        return self.consoleLog

    def finalGainCheck(self):
       pass

    def update(self):
        pass

    # Main menu option 1
    def systemChecks(self):
        output = []
        for key in self.checks:
            if (self.checkTries < 3):
                self.checks[key] = random.choices([True, False])
                self.checkTries += 1
            elif (self.checkTries > 3):
                self.checkTries = 0
                self.checks[key] = True
            if (self.checks[key]):
                output.append("The SimCrafts current " + key + " status is Reached")
            else:
                output.append("The SimCrafts current " + key + " status is not reached")
        return output

    # Main menu option 2
    def verifySignal(self):
        output = []
        if (self.currentGain >= self.gainRange[0]) and (self.currentGain <= self.gainRange[1]):
            self.checks['Antenna Status'] = True
        elif self.currentGain > self.gainRange[1]:
            output.append('UNWANTED HARMONICS DETECTED — gain too high! Reset gain')
        else:
            output.append('UNABLE TO CAPTURE SIGNAL — increase gain to 38 dB')
        return output

    # Main menu option 3    
    def increaseGain(self, newGin):
        output = []
        output.append('GAIN CHANGING -- Please wait...')
        output.append("Gain changed by " + str(abs(newGin)))
        self.currentGain += abs(newGin)
        return output
    
    # Main menu option 4
    def resetGain(self):
        output = []
        output.append("GAIN RESETTING -- Please wait...")
        output.append("Gain reset to 36 dB")
        self.currentGain = 36
        return output
    
    # Main menu option 5
    # telemetryData needs to be passed from SimObject
    def downloadTelemetryData(self):
        output = []
        index = 1
        self.allTelemetryDataGood = True
        for key in self.allTelemetryData:
            if self.allTelemetryData[key]:
                output[index] = "" + key + " Telemetry...COMPLETE!"
            else:
                output[index] = "" + key + " Telemetry...INCOMPLETE!"
                self.allTelemetryDataGood = False
            index += 1
        if (self.allTelemetryDataGood):
            output.append("The Subsystem Telemetry Data has been successfully downloaded!")
        else:
            output.append("Some subsystems have not complete their missions yet and need to send their telemetry data to finish your task.")
        return output

    # Main menu option 6
    def processTelemetryData(self):
        if self.allTelemetryDataGood:
            return "All telemetry data has been successfully processed!"
        else:
            return "Some subsystems have not complete their missions yet and need to send their telemetry data to finish your task."

    # Main menu option 7
    ### NOT DONE!! NEED IMAGE URL ####
    def displayImage(self):
        output = []
        if self.allTelemetryDataGood:
            output[0] = "All telemetry data has been successfully processed!"
            output[1] = "Click the link to view the image!"
            # Rick roll link for shits and giggles
            output[2] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            output[3] = "GREAT WORK ON THE COMMS SYSTEM CONSOLE"
            output[4] = "Mission accomplished!"
            output[5] = "Just kidding...heres the actual image: CARLY_MAKE_URL"
        else:
            output[0] = "Some subsystems have not complete their missions yet and need to send their telemetry data to finish your task."
            
        return output

