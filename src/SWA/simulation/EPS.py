from simulation.Subsystem import Subsystem
from simulation import EPSSolarPanelCharging as Charging
from simulation import EPSInitializing as EPSStart
from simulation import EPSPowerDistribution as PD
from datetime import datetime
import random

class EPS(Subsystem):

    def __init__(self, dicts):
        super().__init__(dicts)
        self.params = {'total power' : EPSStart.initialize(),
                       'available power' : EPSStart.initialize(),
                       'expended power' : 0.0,
                       'battery capacity' : Charging.setupBatteries(),
                       'current battery charge' : Charging.setupBatteries(),
                       'time of last check' : datetime.now(),
                       'simcraft power restrictions' : {},
                       'power distribution' : {},
                       'solar panel angle' : Charging.generateRandomAngle()
                       }
        self.checks = {'Uplink' : random.choice([True, False]),
                       'Bus Connection' : random.choice([True, False]),
                       'Articulation Gear' : random.choice([True, False])}
        self.allChecks = False
        self.params['simcraft power restrictions']['ACS'] = self.params['total power'] * (self.dicts["ACS"]['max power'] / 100)
        self.params['simcraft power restrictions']['EPS'] = self.params['total power'] * (self.dicts["EPS"]['max power'] / 100)
        self.params['simcraft power restrictions']['TCS'] = self.params['total power'] * (self.dicts["TCS"]['max power'] / 100)
        self.params['simcraft power restrictions']['COMMS'] = self.params['total power'] * (self.dicts["COMMS"]['max power'] / 100)
        self.verifyStatus = False
        print("New instance of EPS class created")

    #EPS function for easy power updating ###############################
    def updatePowerParams(self, availablePower, expendedPower, powerDistributed, subsystemName):
        self.params['avialble power'] = availablePower
        self.params['expended power'] = expendedPower
        self.params['power distribution'][subsystemName] = powerDistributed

    #EPS time updates
    def updateTimeParams(self):
        self.params['time of last check'] = datetime.now()

    #EPS Power Generating ###############################################
    def updateBatteryStatus(self):
        self.params['current battery charge'] = Charging.updateBatteryStatus(self.params)
        self.updateTimeParams()

    #EPS Solar Panel Angle
    def articulateAngle(self, delta):
        self.params['solar panel angle'] += delta

    #EPS Power Distribution #############################################
    def requestPower(self, requestedPower, subsystemName):
        # Call to request power from EPS
        requestedPower, availablePower, expendedPower, powerDistributed = PD.requestPower(requestedPower, subsystemName, self.params)
        if requestedPower is None: return 0
        if availablePower is None:
            self.updatePowerParams(availablePower, expendedPower, powerDistributed, subsystemName)
        return requestedPower

    def returnPower(self, returnedPower, subsystemName):
        # Call to return power to EPS
        availablePower, expendedPower, powerDistributed = PD.returnPower(returnedPower, self.params, subsystemName)
        self.updatePowerParams(availablePower, expendedPower, powerDistributed, subsystemName)

    #EPS Console Commands ##################################################
    def systemChecks(self):
        badChecks = [key for key, value in self.checks.items() if not value]
        if not badChecks:
            print("No errors found")
            self.allChecks = True
        else:
            print("ERROR FOUND with :")
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
        print("Verifying Spacecraft power level. Please wait .....")
        expendedPower = self.params['expended power']
        totalPower = self.params['total power']
        checkpoint = 0.8 * totalPower
        currentOperating = expendedPower / checkpoint
        if checkpoint > currentOperating:
            print(f"The spacecraft is currently operating at {1}% power", currentOperating * 100)
            print("100% power is required for this mission activity")
            print("Please set the power to 100%")
            return
        self.verifyStatus = True
        print("Verifying Power...")
        print("Spacecraft now operating at 100% power")

    def fullPower(self):
        print(f"The current solar panel angle is: {1} degrees (away from the sun)" )
        if self.params['solar panel angle'] > 10.0:
            print("Solar panels must be within 10 degrees of the sun angle for increased power to the spacecraft")
            return
        self.params['expended power'] = 0.8 * self.params['total power'] #THIS 100% NEEDS TO BE CHANGED TO ACTUALLY SEND OUT POWER, THIS IS JUST FOR TESTING RIGHT NOW UNTIL OTHER SUBSYSTEMS ARE DONE
        
    def articulate(self, delta):
        self.articulateAngle(delta)
        print("New angle is : ", self.params['solar panel angle'])
    
    def telemtryTransfer(self):
        if self.verifyStatus:
            print("Transferring EPS telemetry. Please wait...")
        else:
            print("Verification process for EPS not completed")
    
    #Comms calls this function #######################################
    def commsConfirmation(self):
        if self.verify:
            return True
        else:
            self.telemtryTransfer()
            return False