from simulation.Subsystem import Subsystem
import random

class TCS(Subsystem):

    def __init__(self, dicts):
        super().__init__(dicts)
        self.orient = {
            'Batteries' : 0,
            'On-Board Computer' : 0,
            'Propulsion' : 0,
            'Reaction Wheels' : 0,
            'Solar Panels' : 0
        }
        ##NEEDS TO BE CHANGED BASED ON TEST CONDUCTOR INPUT -- just have it set as a random goal for now
        self.orientGoal = {
            'Batteries' : random.randint(10,30),
            'On-Board Computer' : random.randint(-20,50),
            'Propulsion' : random.randint(-5,30),
            'Reaction Wheels' : random.randint(-10,50),
            'Solar Panels' : random.randint(-80,80)
        }
        self.orientEqual = True

        self.checks = {
                       'Heating Elements' : random.choice([True, False]),
                       'Bus Connection' : random.choice([True, False]),
                       'Telemetry Signal' : random.choice([True, False])
        }
        self.allChecks = False

        self.targetStatus = {'Ready' : False,
                             'Verify TCS Status' : False,
                             'Activate Cooling Procedure' : False,
                             'Activate Heating Procedure' : False}
        self.verifyStatus = False
        print('New instance of TCS class created')
        self.randomThermal()

    def randomThermal(self):
        for key,value in self.orient:
            self.orient[key] = random.randint(-100,100)

    ############# COOLING ###################
    def updateBattCool(self, newBatt):
        self.orient['Batteries'] -= newBatt
        return ("Battery temperatures cooled to" + newBatt + "degrees")
    
    def updateComputerCool(self, newComp):
        self.orient['On-Board Computer'] -= newComp
        return ("On-Board Computer temperature cooled to" + newComp + "degrees")
    
    def updatePropCool(self, newProp):
        self.orient['Propulsion'] -= newProp
        return ("Propulsion temperatures cooled to" + newProp + "degrees")
    
    def updateReacCool(self, newReac):
        self.orient['Reaction Wheels'] -= newReac
        return ("Reaction Wheels temperature cooled to" + newReac + "degrees")
    
    def updateSolarCool(self, newSolar):
        self.orient['Solar Panels'] -= newSolar
        return ("Propulsion temperatures cooled to" + newSolar + "degrees")
    
    ############## HEATING ######################
    def updateBattHeat(self, newBatt):
        self.orient['Batteries'] += newBatt
        return ("Battery temperatures heated to" + newBatt + "degrees")
    
    def updateComputerHeat(self, newComp):
        self.orient['On-Board Computer'] += newComp
        return ("On-Board Computer temperature cooled to" + newComp + "degrees")
    
    def updatePropHeat(self, newProp):
        self.orient['Propulsion'] += newProp
        return ("Propulsion temperatures heated to" + newProp + "degrees")
    
    def updateReacHeat(self, newReac):
        self.orient['Reaction Wheels'] += newReac
        return ("Reaction Wheels temperature heated to" + newReac + "degrees")
    
    def updateSolarHeat(self, newSolar):
        self.orient['Solar Panels'] += newSolar
        return ("Propulsion temperatures heated to" + newSolar + "degrees")

    def update(self):
        for key,value in self.orient:
            self.orient[key] += round(random.uniform(-.5,5), 1)

    ########## FINAL TEMP CHECK ###############
    def checkFinalTemp(self):
        if self.orient['Batteries'] in range(self.orientEqual['Batteries']+10,self.orientEqual['Batteries']+30):
            print("BATTERIES: VALID")
        else:
            print(f"BATTERIES: INVALID, currently {self.orient['Batteries']} needs to be between 10 and 30")
            return False
        if self.orient['On-Board Computer'] in range(self.orientEqual['On-Board Computer']-20,self.orientEqual['On-Board Computer']+50):
            print("ON-BOARD COMPUTER: VALID")
        else:
            print(f"ON-BOARD COMPUTER: INVALID, currently {self.orient['On-Board Computer']} needs to be between -20 and 50")
            return False
        if self.orient['Propulsion'] in range(self.orientEqual['Propulsion']-5,self.orientEqual['Propulsion']+30):
            print("PROPULSION: VALID")
        else:
            print(f"PROPULSION: INVALID, currently {self.orient['Propulsion']} needs to be between -5 and 30")
            return False
        if self.orient['Reaction Wheels'] in range(self.orientEqual['Reaction Wheels']-10,self.orientEqual['Reaction Wheels']+50):
            print("REACTION WHEELS: VALID")
        else:
            print(f"REACTION WHEELS: INVALID, currently {self.orient['Reaction Wheels']} needs to be between -10 and 50")
            return False
        if self.orient['Solar Panels'] in range(self.orientEqual['Solar Panels']-80,self.orientEqual['Solar Panels']+80):
            print("SOLAR PANELS: VALID")
        else:
            print(f"SOLAR PANELS: INVALID, currently {self.orient['Propulsion']} needs to be between -5 and 30")
            return False
        return True
    
    ###################TCS CONSOLE COMMANDS #######################
    def systemChecks(self):
        badChecks = [key for key, value in self.checks.items() if not value]
        if not badChecks:
            print("No errors found")
            self.allChecks = True
        else:
            print("ERROR FOUND with :")
            for key in badChecks:
                print(key)
            print("Enter refresh to reset the system and re-start system checks")
        print("Enter 'go' if all systems are ready")

    def refresh(self):
        self.checks = {key: True for key in self.checks}

    def verify(self):
        if not self.allChecks:
            print('All system checks not completed')
            return
        print('Verifying spacecraft thermal levels. Please wait .....')
        self.verifyStatus = True
        print('Verifying Thermals...')
        print('TCS now ready for use')

    def tcsStatus(self):
        if not self.targetStatus ['Ready']:
            print('Please verify the system before attempting to initialize TCS status')
            return
        print('Verifying TCS status. Please wait...')
        if self.checkFinalTemp():
            self.targetStatus['Verify TCS Status'] = True
        else:
            print('Invalid component temperatures. Inititate either Cooling or Heating procedures.')

    def coolActivate(self):
        if not self.targetStatus ['Ready']:
            print('Please verify system before attemping to initiate cooling procedure')
            return
        print('Activating Cooling Procedure...')
        userChoiceCool = input(f'Please choose a component to cool: \n1 - Batteries \n2 - On-Board Computer \n3 - Propulsion \n4 - Reaction Wheels \n5 - Solar Panels')
        if userChoiceCool == '1':
            userBatt = input(f'Enter degrees to cool batteries by: ')
            self.updateBattCool(userBatt)
        elif userChoiceCool == '2':
            userComp = input(f'Enter degrees to cool on-board computer by: ')
            self.updateComputerCool(userComp)
        elif userChoiceCool == '3':
            userProp = input(f'Enter degrees to cool propulsion by: ')
            self.updatePropCool(userProp)
        elif userChoiceCool == '4':
            userReac = input(f'Enter degrees to cool reaction wheels by: ')
            self.updateReacCool(userReac)
        elif userChoiceCool == '5':
            userSolar = input(f'Enter degrees to cool solar panels by: ')
            self.updateSolarCool(userSolar)
        else:
            print('Please reenter a valid response')
            self.coolActivate()

    def heatActivate(self):
        if not self.targetStatus ['Ready']:
            print('Please verify system before attemping to initiate heating procedure')
            return
        print('Activating Heating Procedure...')
        userChoiceHeat = input(f'Please choose a component to cool: \n1 - Batteries \n2 - On-Board Computer \n3 - Propulsion \n4 - Reaction Wheels \n5 - Solar Panels')
        if userChoiceHeat == '1':
            userBatt = input(f'Enter degrees to heat batteries by: ')
            self.updateBattHeat(userBatt)
        elif userChoiceHeat == '2':
            userComp = input(f'Enter degrees to heat on-board computer by: ')
            self.updateComputerHeat(userComp)
        elif userChoiceHeat == '3':
            userProp = input(f'Enter degrees to heat propulsion by: ')
            self.updatePropHeat(userProp)
        elif userChoiceHeat == '4':
            userReac = input(f'Enter degrees to heat reaction wheels by: ')
            self.updateReacHeat(userReac)
        elif userChoiceHeat == '5':
            userSolar = input(f'Enter degrees to heat solar panels by: ')
            self.updateSolarHeat(userSolar)
        else:
            print('Please reenter a valid response')
            self.heatActivate()

    def compareOutcome(self):
        for k in self.orient:
            if not self.orient[k] == self.orientGoal[k]:
                print(f'{k} are not equal')
                return
        self.verifyStatus = True
   
    def telemtryTransfer(self):
        if self.verifyStatus:
            print('Transferring TCS telemetry. Please wait...')
        else:
            print('Verification process for COMMS not completed')
            
    def commsConfirmation(self):
        if self.verify:
            return True
        else:
            self.telemtryTransfer()
            return False 