import numpy as np
import math
import random
import EPSInitializing as EPSStart
from datetime import datetime

currentTime = 0.0
tol = 1e-3
#General Functions######################################################
def checkCurrentTime():
    global currentTime
    currentTime = datetime.now()

def reasonableNumbers(input):
    if input < tol:
        input = 0
    else:
        input = round(input,3)
    return input

def checkAngle(angle):
    angle = np.deg2rad(angle)
    while angle >= 2 * np.pi:
        angle = angle - 2*np.pi
    while angle < 0.0:
        angle = angle + 2*np.pi
    return np.rad2deg(angle)

def checkAngleDeg(angle):
    while angle >= 360:
        angle = angle - 360
    while angle < 0:
        angle = angle + 360
    return angle

def deltaAngle(angle1, angle2):
    deltaAngle = np.abs(angle1 - angle2)
    deltaAngle = checkAngle(deltaAngle)     #Doesn't change math, but for bug checking it's nice to look at angles
    return deltaAngle

#Initialization ##############################################################

def setupBatteries(period=3600):    #Default period of one hour in seconds
    #Period is total amount of time taken to do a full orbit, and batteries need to be able to store charge during half the period where the simcraft has no sun
    batteryCapacity = np.ceil(EPSStart.initialize() * (period / 2))   #If there is a buffer, it is already included
    return batteryCapacity

def generateRandomAngle():
    angle = random.uniform(0,360)
    angle = round(angle * 2) / 2
    return angle

#Power Generating ############################################################

def incidentPower(params):
    angle = np.deg2rad(params['angle'])
    if angle >= np.pi: return 0.0
    dt = currentTime - params['time of last check']
    energyGenerated = reasonableNumbers(params['total power'] * np.sin(angle) * dt)
    return energyGenerated

def getEnergyGenerated(params):
    energyGenerated = incidentPower(params)
    return energyGenerated

#Batteries########################################################################

def calculateEnergyDrained(params):
    energyDrained = (params['time of last check'] - currentTime) * params['expended power']
    return energyDrained

#Returns back to EPS.py ############################################################

def updateBatteryStatus(params):
    currentCharge = params['current battery charge']
    checkCurrentTime()
    currentCharge += getEnergyGenerated(params)
    currentCharge -= calculateEnergyDrained(params)
    return currentCharge

def main():
    pass

if __name__ == "__main__":
    main()

