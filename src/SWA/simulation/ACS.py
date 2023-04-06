from Subsystem import Subsystem
import random

class ACS(Subsystem):

    def __init__(self, dicts):
        super().__init__(dicts)
        self.dicts = dicts
        self.orient = {
           "roll":0,
           "pitch":0,
           "yaw": 0
        }
         ##NEEDS TO BE CHANGED BASED ON TEST CONDUCTOR INPUT -- just have it set as a random goal for now
        self.orientGoal = {
            'roll' : random.randint(-180,180),
            'pitch' : random.randint(-180,180),
            'yaw' : random.randint(0,90)
        }

        self.orientEqual = True

        self.checks = {
                       'Control Moment Gyros' : random.choice([True, False]),
                       'Attitude Stability' : random.choice([True, False]),
                       'S-Band Antenna B' : random.choice([True, False])
        }
        self.allChecks = False
        self.targetStatus = {'Ready' : False,
                             'Verify CMG Status' : False,
                             'Activate CMG Maneuver' : False,
                             'Verify Alignment' : False}
        self.verifyStatus = False
        print("New instance of ACS class created")
        self.randomRollPitchYaw()

    def randomRollPitchYaw(self):
        for key,value in self.orient:
            self.orient[key] = random.randint(-180,180)
        self.orient['pitch'] = random.randint(-90,90)
    
    def updateRoll(self, newRoll):
        self.orient['roll'] += newRoll
        return ("Roll updated by" + newRoll + "degrees")
    
    def updatePitch(self, newPitch):
        self.orient['pitch'] += newPitch
        return ("Pitch updated by" + newPitch + "degrees")
    
    def updateYaw(self, newYaw):
        self.orient['yaw'] += newYaw
        return ("Yaw updated by" + newYaw + "degrees")

    def update(self):
        for key,value in self.orient:
            self.orient[key] += random.randint(-1,1)
            if (self.orient[key]>180) or (self.orient[key]<-180):
                self.orient[key]=0
        self.orient['pitch'] += random.randint(-1,1)
        if (self.orient[key]>90):
            self.orient[key]=0
        elif(self.orient[key]<0):
            self.orient[key]=90


    def checkFinalRPY(self):
        if self.orient['roll'] in range(self.orientEqual['roll']-70,self.orientEqual['roll']+70):
            print("ROLL: VALID")
        else:
            print(f"ROLL: INVALID, currently {self.orient['roll']} needs to be between -70 and 70")
            return False
        if self.orient['pitch'] in range(self.orientEqual['pitch']-90,self.orientEqual['pitch']+65):
            print("PITCH: VALID")
        else:
            print(f"PITCH: INVALID, currently {self.orient['pitch']} needs to be between -90 and 65")
            return False
        if self.orient['yaw'] in range(self.orientEqual['yaw']-25,self.orientEqual['yaw']+15):
            print("YAW: VALID")
        else:
            print(f"YAW: INVALID, currently {self.orient['YAW']} needs to be between -25 and 15")
            return False
        return True
    
    ###################ACS CONSOLE COMMANDS #######################
    def systemChecks(self):
        badChecks = [key for key,value in self.checks.items() if not value]
        print(badChecks)
        if not badChecks:
            print("No errors found")
            self.allChecks = True
        else:
            print("ERROR FOUND with :")
            for key in badChecks:
                print(key)
            print("Enter 'refresh' to reset the system and re-start system checks")
        print("Enter 'go' if all systems are ready")

    def refresh(self):
        self.checks = {key: True for key in self.checks}

    def verify(self):
        if not self.allChecks:
            print('All system checks not completed')
            return
        self.targetStatus['Ready'] = True
        print('Verifying ACS...')
        print('ACS now ready for use')

    def cmgStatus(self):
        if not self.targetStatus['Ready']:
            print('Please verify the system before attempting to initialize CMG status')
            return
        print('Verifying CMG status. Please wait...')
        if self.checkFinalRPY():
            self.targetStatus['Verify CMG Status'] = True
        else:
            print('Invalid values for Degrees of Freedom. Inititate CMGs.')

    def cmgActivate(self):
        if not self.targetStatus['Ready']:
            print('Please verify the system before attempting to initialize CMG status')
            return
        print ('Activating CMGs...')
        userChoiceCMG = input(f'Please choose a Degree of Freedom to alter: \n1 - Roll \n2 - Pitch \n3 - Yaw')
        if userChoiceCMG == '1':
            userRoll = input(f'Enter magnitude of roll manuever: ')
            self.updateRoll(userRoll)
        elif userChoiceCMG == '2':
            userPitch = input(f'Enter magnitude of pitch manuever: ')
            self.updatePitch(userPitch)
        elif userChoiceCMG == '3':
            userYaw = input(f'Enter magnitude of yaw manuever: ')
            self.updateYaw(userYaw)
        else:
            print('Please reenter a valid response')
            self.cmgActivate()
        
    def compareOutcome(self):
        for k in self.orient:
            if not self.orient[k] == self.orientGoal[k]:
                print(f'{k} are not equal')
                return
        self.verifyStatus = True
   
    def telemtryTransfer(self):
        if self.verifyStatus:
            print('Transferring ACS telemetry. Please wait...')
        else:
            print('Verification process for COMMS not completed')
            
    def commsConfirmation(self):
        if self.verify:
            return True
        else:
            self.telemtryTransfer()
            return False 

            