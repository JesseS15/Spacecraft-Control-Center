from simulation.Subsystem import Subsystem
import random

class COMMS(Subsystem):

    checks = {
        "On-board Computer": True,
        "Antenna Status": True
    }

    frequency = random.randrange(12.0, 18.0)
    gain = random.randrange(25, 30)
    frequencyRange = [12.0, 18.0]
    gainRange = [25, 30]
    allTelemetryDataGood = False

    def __init__(self):
        super().__init__()
        print('New instance of COMMS class created')

    def update(self):
        pass

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
    def downloadTelemetryData(self, telemetryData):
        output = []
        index = 1
        self.allTelemetryDataGood
        for key in telemetryData:
            if telemetryData[key]:
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
    def displayImage(self):
        pass

