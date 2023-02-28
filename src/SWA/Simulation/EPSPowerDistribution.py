import numpy as np
import EPSInitializing as EPSStart
import EPSSolarPanelCharging as charging

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

    N

'''

#Global variable
totalPower = EPSStart.initialize()     

def checkPowerRequirements():
    global totalPower
    totalPower = EPSStart.initialize()

def subsystemPowerRequirements(subsystemName, subsystemRequiredPower):
    simcraftSubsystemPower = {subsystemName : subsystemRequiredPower}

def requestPower(powerRequested):
    pass

def checkPower():
    pass

def sendPower(requestedPower):
    power = 0
    return power

def main():
    checkPowerRequirements()

if __name__ == "__main__":
    main()