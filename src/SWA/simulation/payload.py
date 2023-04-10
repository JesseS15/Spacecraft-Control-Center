from simulation.Subsystem import Subsystem
import random

class payload(Subsystem):

    payloadName = "Payload"
    checks = {
            'Optical Electronics' : random.choice([True, False]),
            'Bus Connection' : random.choice([True, False]),
            'Gimble Connection' : random.choice([True, False])
        }
    
    targetStatus = {
        'Ready' : False,
        'Slew Imager' : False,
        'Acquire Target' : False,
        'Capture Target' : False
        }
    allChecks = False
    verifyStatus = False

    def __init__(self, payloadName):
        super().__init__()
        self.payloadName = payloadName

    def payloadAction(self):
        print("Payload action")

    #Returns for UI ##########################################################################
    def UIReturns(self):
        UI = {'payload checks' : self.checks,
              'target status' : self.targetStatus,
              'payload telem status' : self.verifyStatus}
        return UI

    #Payload console commands ################################################################

    def systemChecks(self):
        badChecks = [key for key, value in self.checks.items() if not value]
        if not badChecks:
            print("No erros found")
            self.allChecks = True
        else:
            print("ERROR FOund with :")
            for key,value in badChecks:
                print(key)
            print("Enter 'refresh' to reset the system and re-start system checks")
        print("Enter 'go' if all systems are ready")

    def refresh(self):
        self.checks = {key: True for key in self.checks}

    def verify(self):
        if not self.allChecks:
            print('All system checks not completed')
            return
        self.targetStatus['ready'] = True
        print('Verifying Payload...')
        print('Payload now ready for use')
        
    def slewImager(self):
        if not self.targetStatus['ready']:
            print('Please verify the system before attempt to slew image')
            return
        print('Slew commencing. Please wait...')
        self.targetStatus['Slew Imager'] = True
        print('The imager has reached the ground target area')
        print('Enter "acquire target" command for ground target acquisition')
    
    def acquireTarget(self):
        if not self.targetStatus['Slew Imager']:
            print('Please slew image before attempting to acquire the target')
            return
        self.targetStatus['Acquire Target'] = True
        print('Target acquisition commencing. Please wait...')
        print('Enter "capture target" command for for gorund target acquisition')
    
    def captureImage(self):
        if not self.targetStatus['Acquire Target']:
            print('Please acquire the target before attempting to capture the target')
            return
        self.targetStatus['Capture Image'] = True
        print('Image capture commencing. Please wait...')
        print('The ground target image has been captured successfully')

    def telemtryTransfer(self):
        if self.verifyStatus:
            print('Transferring EPS telemetry. Please wait...')
        else:
            print('Verification process for Comms not completed')
    
    #Comms calls this functions #######################################
    def commsConfirmation(self):
        if self.verify:
            return True
        else:
            self.telemtryTransfer()
            return False    
        
    def update():
        pass
