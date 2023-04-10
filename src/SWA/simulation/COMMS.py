from simulation.Subsystem import Subsystem
import random

class COMMS(Subsystem):

    checks = {
        'signal' : random.choice([True, False]),
        'telem' : False,
        'processing' : False
        }
        
    systemChecksList = {
        'EPS' : False,
        'TCS' : False,
        'ACS' : False,
        'COMMS' : False
        }
    payloadCheck = False
    verify = False

    def __init__(self):
        super().__init__()
        self.gain = 1
        self.requiredGain = random.randint(1, 10)
        print('New instance of COMMS class created')

    def update():
        pass

    #Comms Attribute internal commands
    def updateGain(self, update):
        self.gain = update
        print("Gain has been adjusted")

    def systemChecks(self, subsystemName, status):
        self.systemChecksList[subsystemName] = status

    #Returns for UI################################################
    def UIReturns(self):
        UI = {'subsystem telemetry status' : self.systemChecksList,
              'gain' : self.gain,
              'RPY': self.RPY,
              'comms telem status' : self.checks['telem']
              }
        return UI

    #Comms Console Commands #######################################
    def verifySignalLock(self):
        if self.checks['signal']:
            print('Ku-Band signal is locked on')
        else:
            print('ERROR FOUND')
            print('Ku-Band signal is degraded')
            print('Atmospheric attenuation requires enhanced signal power')
            print('Enter command "gain adjust" to reduce signal attenuation')

    def gainAdjust(self):
        self.checks['signal'] = True
        print('Antenna gain adjustment commencing. Please wait...')
        print('Ku-Band signal is transmitting nominally')
        if not self.checks['signal']:
            print('Ku-Band signal is unstable, please fix this before attempting')
            return

    def verifyTelemDownload(self):
        print('Imaging download being interrogated. Please wait...')
        print('Imaging telemtry downloaded nominally')
        self.checks['telem'] = True

    def processImageTelem(self):
        if not self.checks['telem']:
            print('Please verify telemetry download before attempting to process the image')
            return
        print('Image processing commencing. Please wait...')
        print('Full image processing is complete')
        self.checks['processing'] = True

    def displayImage(self):
        if not self.checks['processing']:
            print('Please process the image before attempting to display')
            return
        print('Displaying image. Please wait...')
        #Something here that displays the image...
