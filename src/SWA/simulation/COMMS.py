from simulation.Subsystem import Subsystem
import random

class COMMS(Subsystem):

    def __init__(self, dicts):
        super().__init__(dicts)
        self.attributes = self.dicts['COMMS']
        self.gain = 1
        self.checks = {'signal' : random.choice([True, False]),
                       'telem' : False,
                       'processing' : False}
        self.verify = False
        print('New instance of COMMS class created')

<<<<<<< Updated upstream
    def update():
        pass
=======
    def gainControl(self, input):
        self.gain = input
        print("Gain has been adjusted")
>>>>>>> Stashed changes

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

    def verifyTelemDownload(self):
        if not self.checks['signal']:
            print('Ku-Band signal is unstable, please fix this before attempting')
            return
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
