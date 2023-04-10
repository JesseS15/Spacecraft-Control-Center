from simulation.Subsystem import Subsystem
import random

class COMMS(Subsystem):

    checks = {
        "On-board Computer": True,
        "Antenna Status": True
    }

    frequency = random.randrange(12.0, 18.0)
    frequencyRange = [12.0, 18.0]

    gain = random.randrange(25, 30)
    gainRange = [25, 30]

    allTelemetryDataGood = False
    allTelemetryData = {"ACS": False, "EPS": False, "TCS": False, "Payload": False}

    commands = [
        "WELCOME TO THE COMMUNICATIONS (COMMS) CONSOLE",
        "Your task is to verify that signal lock is established between the Ku-Band satellite antenna and the ground station antenna, transmit the target image to the ground station, process the image, and display the results.",
        "1.) Status Checks",
        "2.) Verify Signal",
        "3.) Signal Gain",
        "4.) Signal Frequency",
        "5.) Download Telemetry Data",
        "6.) Process Telemetry Data",
        "7.) Display Image"
    ]

    def __init__(self):
        super().__init__()
        print('New instance of COMMS class created')

    def update(self):
        self.gain += random.randrange(-5.0, 5.0)

    # Main menu option 1
    def systemChecks(self):
        output = []
        index = 0
        for key in self.checks:
            self.checks[key] = bool(random.getrandbits(1))
            if (self.checks[key]):
                output[index] = "The SimCrafts current " + key + "status is Reached"
            else:
                output[index] = "The SimCrafts current " + key + "status is not reached"
        return output

    # Main menu option 2
    def verifySignal(self):
        output = []
        if (self.frequency < self.frequencyRange[0] or self.frequency > self.frequencyRange[1]):
            output[0] = "The SimCrafts current signal frequency is OUTSIDE the required bandwidth of 12.000-18.000 GHz"
        else:
            output[0] = "The SimCrafts current signal frequency is INSIDE the required bandwidth of 12.000-18.000 GHz"
        
        if (self.gain < self.gainRange[0] or self.gain > self.gainRange[1]):
            output[1] = "The SimCrafts current signal gain is OUTSIDE the required strength of 25-30 dB"
        else:
            output[1] = "The SimCrafts current signal gain is INSIDE the required strength of 25-30 dB"
        
        return output

    # Main menu option 3
    def signalGain(self, newGain):
        self.gain += newGain
        return ("Gain has changed by " + newGain + "dB")

    # Main menu option 4
    def signalFrequency(self, newFreq):
        self.frequency += newFreq
        return ("Frequency has changed by " + newFreq + "GHz")

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
            output[0] = "The Subsystem Telemetry Data has been successfully downloaded!"
        else:
            output[0] = "Some subsystems have not complete their missions yet and need to send their telemetry data to finish your task."
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
        if self.allTelemetryDataGood:
            output = []
            output[0] = "All telemetry data has been successfully processed!"
            output[1] = "Click the link to view the image!"
            # Rick roll link for shits and giggles
            output[2] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            output[3] = "GREAT WORK ON THE COMMS SYSTEM CONSOLE"
            output[4] = "Mission accomplished!"
            output[5] = "Just kidding...heres the actual image: CARLY_MAKE_URL"
            return output
        else:
            return "Some subsystems have not complete their missions yet and need to send their telemetry data to finish your task."

