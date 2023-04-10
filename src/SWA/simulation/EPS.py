import Subsystem
import EPSSolarPanelCharging as Charging
import EPSInitializing as EPSStart
import EPSPowerDistribution as PD
from datetime import datetime
import random

class EPS(Subsystem):

    params = {
        'total power' : EPSStart.initialize(),
        'available power' : EPSStart.initialize(),
        'expended power' : 0.0,
        'battery capacity' : Charging.setupBatteries(),
        'current battery charge' : Charging.setupBatteries(),
        'time of last check' : datetime.now(),
        'simcraft power restrictions' : {'EPS' : 0.0,
                                        'TCS' : 0.0,
                                        'COMMS' : 0.0,
                                        'ACS' : 0.0,
                                        'Payload' : 0.0},
        'power distribution' : {'EPS' : 0.0,
                                'TCS' : 0.0,
                                'COMMS' : 0.0,
                                'ACS' : 0.0,
                                'Payload' : 0.0},
        'solar panel angle' : Charging.generateRandomAngle()
        }  
    
    checks = {
        'Uplink' : random.choice([True, False]),
        'Bus Connection' : random.choice([True, False]),
        'Articulation Gear' : random.choice([True, False])
        }
    
    allChecks = False
    verifyStatus = False

    def __init__(self):
        super().__init__()
        self.params['simcraft power restrictions']['ACS'] = self.params['total power'] * 0.16
        self.params['simcraft power restrictions']['EPS'] = self.params['total power'] * 0.16
        self.params['simcraft power restrictions']['TCS'] = self.params['total power'] * 0.16
        self.params['simcraft power restrictions']['COMMS'] = self.params['total power'] * 0.16
        self.params['simcraft power restrictions']['COMMS'] = self.params['total power'] * 0.16
        print("New instance of EPS class created")

    def update(self):
        self.updateTimeParams()
        self.updatePowerParams()
        self.updateBatteryStatus()

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
        self.params['solar panel angle'] += Charging.checkAngleDeg(delta)

    #EPS Power Distribution #############################################
    def requestPower(self, requestedPower, subsystemName):
        # Call to request power from EPS
        availablePower, expendedPower, powerDistributed = PD.requestPower(requestedPower, subsystemName, self.params)
        if requestedPower is None: return 0
        if availablePower is None:
            self.updatePowerParams(availablePower, expendedPower, powerDistributed, subsystemName)
        return requestedPower

    def returnPower(self, returnedPower, subsystemName):
        # Call to return power to EPS
        availablePower, expendedPower, powerDistributed = PD.returnPower(returnedPower, self.params, subsystemName)
        self.updatePowerParams(availablePower, expendedPower, powerDistributed, subsystemName)

    def calculateConsumedPower(self):
        powerDistributed = self.params['power distributed']
        total = 0.0
        for key in powerDistributed:
            total += powerDistributed[key]
        self.params['expended power'] = total

    #Returns for UI ########################################################
    def UIReturns(self):
        self.batteryStats = {'battery capacity' : self.params['battery capacity'],
                             'current battery charge' : self.params['current battery charge']}
        UI = {'power distribution' : self.params['power distributed'],
              'battery status' : self.batteryStats,
              'eps telem status' : self.verifyStatus}
        return UI

    #EPS Console Commands ##################################################
    def statusChecks(self):
        badChecks = [key for key, value in self.checks.items() if not value]
        if not badChecks:
            self.allChecks = True
            return("No errors found")
        else:
            returnString="ERROR FOUND with : "
            for key in badChecks:
                returnString+=(key + ", ")
            
    def refresh(self):
        self.checks = {key: True for key in self.checks}

    def verifyPowerDist(self):
        if not self.allChecks:
            return('All system checks not completed')
        expendedPower = self.params['expended power']
        totalPower = self.params['total power']
        checkpoint = 0.8 * totalPower
        currentOperating = expendedPower / checkpoint
        if checkpoint > currentOperating:
            return(f"The spacecraft is currently operating at "+(currentOperating * 100)+"% power\n100% power is required for this mission activity\nPlease set the power to 100%")
        self.verifyStatus = True
        return("Verifying Power...\nSpacecraft now operating at 100% power")
        

    def fullPower(self):
        outputString = []
        outputString.append("The current solar panel angle is: "+self.params['solar panel angle']+" degrees (away from the sun)" )
        if self.params['solar panel angle'] > 10.0:
            outputString.append("Solar panels must be within 10 degrees of the sun angle for increased power to the spacecraft")
            return outputString
        self.calculateConsumedPower()
        if self.params['expended power'] < (self.params['total power'] * 0.8):
            outputString.append('Not all systems running at max power')
        return outputString

    def articulate(self, delta):
        self.articulateAngle(delta)
        return("New angle is : ", self.params['solar panel angle'])
    
    def telemtryTransfer(self):
        if self.verifyStatus:
            return("Data has been Transferred! GREAT WORK ON THE ELECTRICAL POWER SYSTEMS (EPS) CONSOLE")
        else:
            return("Verification process for EPS not completed")
    
    #Comms calls this function #######################################
    def commsConfirmation(self):
        if self.verifyStatus:
            return True
        else:
            self.telemtryTransfer()
            return False