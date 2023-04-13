from simulation.Subsystem import Subsystem
import random

class COMMS(Subsystem):

    checks = {
        "On-board Computer": True,
        "Antenna Status": True
    }

    frequency = random.randrange(12.000, 14.000)
    currentGain = 36 #random.randrange(10, 65)

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
        "4.) Decrease Signal Gain",
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
        
        consoleResponse = []
        
        command_split = command.lower().split(" ")
        
        if self.menu == "tl":
            if command_split[0] == "1":
                consoleResponse.append("Checking Power Systems…")
                consoleResponse.extend(self.systemChecks())
            elif command_split[0] == "2":
                consoleResponse.append("Verifying Signal...")
                consoleResponse.extend(self.verifySignal())
            elif command_split[0] == "3":
                consoleResponse.append("How much do you want to decrease the Signal Gain (in dB)?")
                self.menu = "signalGainDecrease"
            elif command_split[0] == "4":
                consoleResponse.append("How much do you want to change the Signal Frequency (in GHz)?")
                self.menu = "signalFreq"
            elif command_split[0] == "5":
                consoleResponse.append("Downloading Subsystem Telemetry...")
                consoleResponse.extend(self.downloadTelemetryData())
            elif command_split[0] == "6":
                consoleResponse.append("Processing SimCraft Telemetry...")
                consoleResponse.append(self.processTelemetryData())
            elif command_split[0] == "7":
                consoleResponse.append("Displaying Image...")
                consoleResponse.append( self.displayImage())
                consoleResponse.append("GREAT WORK ON THE PAYLOAD SYSTEM CONSOLE!")
                #TODO: create instance where user cannot enter commands after subsys finished
            else:
                consoleResponse.append("Invalid Command " + command)
        
        elif self.menu == "signalGainDecrease":
            consoleResponse.append(newGain(int(command)))
            self.menu = "tl"
    
        elif self.menu == "signalFreq":
            consoleResponse.append(self.signalFrequency(int(command)))
            self.menu = "tl"

        else:
            self.menu = "tl"
            
        self.consoleLog.extend(consoleResponse)
        return self.consoleLog

    def finalGainCheck(self):
       # randomGain = random.randrange(35,37)
       # if (randomGain %2 == 0 ): #final number is even; odd # is harmonic
           # return randomGain
        #else:
            #finalGain = randomGain - 1 #forces even # gain
           return finalGain

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
        if self.checks['Antenna Status'] == False:
          return 'SIGNAL GARBLED! Increase gain to 38 dB and verify the signal again.'
        else:
            return 'Antenna Status: VALID'
        
    def increaseGain(self):
        newGain = input(f'Input gain increase: \n')
        print('GAIN INCREASED -- Please wait...')
        self.currentGain += newGain
        return self.currentGain
    
    def decreaseGain(self):
        self.currentGain -= newGain
        newGain = input(f'Input gain decrease: \n')
        print('GAIN DECREASED -- Please wait...')
        return self.currentGain
    
    def gainReset(self):
        self.currentGain = 36
        return self.currentGain
    
    def checkGain(self):
        if self.currentGain == 38:
            print('SIGNAL CAPTURED. Resetting to original gain...')
            self.gainReset()
            self.checks['Antenna Status'] = True
        elif self.currentGain > 38:
           print('UNWANTED HARMONICS DETECTED — gain too high! Reduce to 38 dB') 
           self.decreaseGain() 
        else:
            print('UNABLE TO CAPTURE SIGNAL — increase gain to 38 dB')
            self.increaseGain()


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

