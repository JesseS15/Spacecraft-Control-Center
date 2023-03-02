


'''
Goal:
    Create a power distribution model that should be easily integratable into the program.

    Charging and power requirements calculators are elsewhere.

Thoughts:
    I've been thinking a point system should work, distributing power on a per point basis.
    Define a point as a percentage of the total power, then whenever a request is received,
    return the amount of power.

    Depending on how power requirements are defined in the subsystem, will determine how
    I'll continue forward with this code. So I need to wait for confirmation back from
    Summer or Jeremy about how power will be defined.

    Taking in two args (name of subsystem, amount of power needed)
    Store these values somewhere somehow

Notes:
    This system has four global variables:
        avaialblePower - total amount of power available for subsytems to request
        expendedPower - total amount of power be consumed
        simcraftSubsystemPower - dictionary containing subsystem names and the corresponding max amount of power they need
        powerDistributed - dictionary containing subysystem names and the corresponding power they are currently consuming

'''

#Global variable
availablePower = 0.0
expendedPower = 0.0
simcraftSubsystemPower = {}
powerDistributed = {}

def initialize(inputWatts=200):
    global availablePower
    availablePower = inputWatts

def subsystemPowerRequirements(subsystemName, subsystemRequiredPower):  #Dictionary of all the subsystems and their power requirements
    global simcraftSubsystemPower
    simcraftSubsystemPower[subsystemName] = subsystemRequiredPower

def checkPower(requestedPower, subsystemName):  #Checks to see if the power requested is a valid amount that subsytem can request
    global simcraftSubsystemPower, powerDistributed
    maxPower = simcraftSubsystemPower[subsystemName]
    if maxPower < requestedPower: 
        pass
    else: 
        return False
    if powerDistributed[subsystemName] + requestedPower < maxPower:
        return True
    else:
        return False 

def sendPower(requestedPower, subsystemName):  #Updates global variables
    global availablePower, expendedPower, powerDistributed
    availablePower -= requestedPower
    expendedPower += requestedPower
    powerDistributed[subsystemName] += requestedPower
    return requestedPower

def requestPower(requestedPower, subsystemName):    #Primary callable function to request power that checks if the request is valid
    if not checkPower(requestedPower, subsystemName): 
        print('Requesting too much power')
        return 
    return sendPower(requestedPower,subsystemName)

def returnPower(returnedPower, subsystemName):  #Returning power back to the EPS 
    global availablePower, expendedPower, powerDistributed
    availablePower += returnedPower
    expendedPower -= returnedPower
    powerDistributed[subsystemName] -= returnedPower

def main():
    initialize()

if __name__ == "__main__":
    main()