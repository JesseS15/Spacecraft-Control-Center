from simulation.Subsystem import Subsystem
import random

class TCS(Subsystem):

    ACSThermal = {
        "CMG": random.randrange(-100,100),
        "Alignment System": random.randrange(-100,100)
    }
    ACSThermalRange = {
        "CMG": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Alignment System": [random.randrange(-100,-20), random.randrange(20, 100)]
    }

    EPSThermal = {
        "Power Distribution": random.randrange(-100,100),
        "Battery": random.randrange(-100,100),
        "Articulation System": random.randrange(-100,100)
    }
    EPSThermalRange = {
        "Power Distribution": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Battery": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Articulation System": [random.randrange(-100,-20), random.randrange(20, 100)]
    }

    COMMSThermal = {
        "On-board Computer": random.randrange(-100,100),
        "Signal Processor": random.randrange(-100,100)
    }
    COMMSThermalRange = {
        "On-board Computer": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Signal Processor": [random.randrange(-100,-20), random.randrange(20, 100)]
    }

    PayloadThermal = {
        "Optical Electronics": random.randrange(-100,100),
        "Gimbal System": random.randrange(-100,100),
        "Imager": random.randrange(-100,100),
    }
    PayloadThermalRange = {
        "Optical Electronics": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Gimbal System": [random.randrange(-100,-20), random.randrange(20, 100)],
        "Imager": [random.randrange(-100,-20), random.randrange(20, 100)]
    }

    SubsystemThermal = {
        "ACS": ACSThermal,
        "EPS": EPSThermal,
        "COMMS": COMMSThermal,
        "Payload": PayloadThermal
    }
    SubsystemThermalRange = {
        "ACS": ACSThermalRange,
        "EPS": EPSThermalRange,
        "COMMS": COMMSThermalRange,
        "Payload": PayloadThermalRange
    }

    checks = {
        'Heating Elements' : random.choice([True, False]),
        'Bus Connection' : random.choice([True, False]),
        'Telemetry Signal' : random.choice([True, False])
    }
    
    telemtryTransferComplete = False

    def __init__(self):
        super().__init__()
        print('New instance of TCS class created')

##### LAST PART ########## increase by 1 degree every 5 seconds
    def randomThermal(self):
        pass

    ###################TCS CONSOLE COMMANDS #######################
    # Main menu option 1
    def checkThermalSystems(self):
        outputString = {}
        for key in self.checks:
            self.checks[key] = random.choice([True, False])
            if self.checks[key]:
                outputString[key] = (key + " -- REACHED")
            else:
                outputString[key] = (key + " -- NOT REACHED, REFRESH SYSTEM")
        return outputString    

    # Main menu option 2 with sub-menu option as subsystem string
    # subsystem must be: "ACS", "EPS", "COMMS", or "Payload"            
    def verifySubsystem(self, subsystem):
        output = []
        index = 0
        for item in self.SubsystemThermalRange[subsystem]:
            lower = self.SubsystemThermalRange[subsystem][item][0]
            upper = self.SubsystemThermalRange[subsystem][item][1]
            current = self.SubsystemThermal[subsystem][item]
            output[index] = item + " current temp = " + current + ". Good range: [" + lower + ", " + upper + "]"
            index += 1
        return output
    
    ############# COOLING ###################
    # Main menu option 3
    # subsystem must be: "ACS", "EPS", "COMMS", or "Payload"
    # item must be exactly as string in dictionaries above
    # amount can be positive or negative number
    def coolSubsystemItem(self, subsystem, item, amount):
        self.SubsystemThermal[subsystem][item] += amount

    # Main menu option 4 - telemtry transfer
    def telemtryTransfer(self):
        if self.allSubsystemsInRange:
            self.telemtryTransferComplete = True
            return True
        else:
            return False
    
    # Main menu option 5 - refresh thermal systems
    def refresh(self):
        for key in self.checks:
            self.checks[key] = True
    
    # Used to check for telemtry transfer
    def allSubsystemsInRange(self):
        for subsys in self.SubsystemThermal:
            for item in self.SubsystemThermal[subsys]:
                lowerRange = self.SubsystemThermalRange[subsys][item][0]
                upperRange = self.SubsystemThermalRange[subsys][item][1]
                itemValue = self.SubsystemThermal[subsys][item]
                if itemValue < lowerRange or itemValue > upperRange:
                    return False
        return True
   
    