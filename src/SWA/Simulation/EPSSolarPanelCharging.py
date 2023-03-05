import numpy as np
import EPSInitializing as EPSStart
import time
from timezonefinder import TimezoneFinder
from datetime import datetime, time
import pytz

#Goal:
'''
The goal of this file is to create a function that will take
inputs like the position of the sun, the orientation of the
simcraft's solar panels, and determine the charging rate of
at that moment in time.

Key Assumptions:
    Strength of the sun's energy is uniform, meaning that being closer
    to the sun will not effect charging rate

    We can represent the orientation of a 3D Vector using two
    polar angles. 

Thoughts:
    We could probably represent the sun as a point on a circle that
    exist solely on the circumference of the circle and the 
    solar panel is at the center of that circle. That way,
    the orientation needs to be changed in terms of that azimuth
    and polar angle.

    Radius from the simcraft does not matter, only care about the
    polar angle and azimuth.

MAIN FUNCTION:
    The primary function someone might want to use is:

    getEnergyGenerated(angle1Sim, angle2Sim, angle1Sun, angle2Sun)

    which will send back how much energy is being generated based on the direction
    the simcraft is facing and the position of the sun relative to it. The assumption
    is that these are spherical coordinates and all inputs should be in radians. 
'''

chargeRate = EPSStart.totalPower        #This is the maximum amount of charge the solar panels will draw, right now it's 2500
CurrentCharge = 0.0
batteryCapacity = 0.0
timeOfLastCheck = np.floor(time.time())
currentTime = 0.0
tol = 1e-3

def checkTime():
    global timeOfLastCheck
    timeOfLastCheck = np.floor(time.time())

def checkCurrentTime():
    global currentTime
    currentTime = np.floor(time.time())

def checkTimeAtSimcraftPosition(lat, lng):
    tf = TimezoneFinder()
    lat = lat
    lng = lng
    timezoneName = tf.timezone_at(lng=lng,lat=lat)
    utcTime = datetime.utcnow()
    utcZone = pytz.utc
    localZone = pytz.timezone(timezoneName)
    localTime = utcZone.localize(utcTime).astimezone(localZone)
    startTime = time(18,0,0)
    endTime = time(6,0,0)
    timeWithinRange = False
    if localTime.time() >= startTime or localTime.time <= endTime:
        timeWithinRange = True
    return timeWithinRange

def reasonableNumbers(input):
    if input < tol:
        input = 0
    else:
        input = round(input,3)
    return input

def checkAngle(angle):
    while angle >= 2 * np.pi:
        angle = angle - 2*np.pi
    while angle < 0.0:
        angle = angle + 2*np.pi
    return angle

def deltaAngle(angle1, angle2):
    deltaAngle = np.abs(angle1 - angle2)
    deltaAngle = checkAngle(deltaAngle)     #Doesn't change math, but for bug checking it's nice to look at angles
    return deltaAngle

def incidentPower(params, chargeRate):  #Puts out a proportional amount of charge generated based on the two angles
    if params['polar'] >= np.pi or params['azimuth'] >= np.pi: return 0.0 #In physical terms, this checks if the sun is behind the face of the solar panels
    if checkTimeAtSimcraftPosition(params['lat'], params['lng']) : return 0.0 #If is night time, then no power is generated
    dt = currentTime - timeOfLastCheck
    energyGenerated = chargeRate * np.sin(params['polar']) * np.sin(params['azimuth']) * dt
    energyGenerated = reasonableNumbers(energyGenerated)
    chargeBatteries(energyGenerated)
    return energyGenerated

def getEnergyGenerated(angle1Sim, angle2Sim, angle1Sun, angle2Sun, lat=0.0, lng=0.0): 
    params =  { 'angle1Sim' : angle1Sim,
                'angle2Sim' : angle2Sim,
                'angle1Sun' : angle1Sun,
                'angle2Sun' : angle2Sun,
                'polar' : None,
                'azimuth' : None,
                'lat' : lat,
                'lng' : lng}
    params['polar'] = deltaAngle(params['angle1Sim'], params['angle1Sun'])
    params['azimuth'] = deltaAngle(params['angle2Sim'], params['angle2Sun'])
    energyGenerated = incidentPower(params, chargeRate)
    return energyGenerated

def setupBatteries(period=3600):    #Default period of one hour in seconds
    #Period is total amount of time taken to do a full orbit, and batteries need to be able to store charge during half the period where the simcraft has no sun
    global batteryCapacity
    batteryCapacity = np.ceil(chargeRate * (period / 2))   #If there is a buffer, it is already included

def drainBatteries(energyDrained):
    global CurrentCharge
    CurrentCharge -= energyDrained
    if CurrentCharge < 0.0:
        CurrentCharge = 0.0

def chargeBatteries(energyGenerated):
    global CurrentCharge
    CurrentCharge += energyGenerated
    if CurrentCharge > batteryCapacity:
        CurrentCharge = batteryCapacity

def calculateEnergyDrained(drainRate):
    energyDrained = (timeOfLastCheck - currentTime) * drainRate
    return energyDrained

def updateBatteryStatus(angle1Sim, angle2Sim, angle1Sun, angle2Sun, drainRate=0.0):
    checkCurrentTime()
    getEnergyGenerated(angle1Sim, angle2Sim, angle1Sun, angle2Sun)
    drainBatteries(calculateEnergyDrained(drainRate))
    checkTime()
    return CurrentCharge

def testcheckAngle():
    print("Testing checkAngle...")
    angle = [0.0, np.pi, 3*np.pi, -np.pi, -3*np.pi]
    expectedResults = [0.0, np.pi, np.pi, np.pi, np.pi]
    results = [1000000.0, 0.0, 0.0, 0.0, 0.0]
    for i, n in enumerate(angle):
        results[i] = checkAngle(n)
    if results != expectedResults:
        print('something went wrong')
        return False
    print("Done")
    return True

def testdeltaAngle():
    print("Testing deltaAngle...")
    angleSim = [0.0, np.pi, -np.pi, np.pi]
    angleSun = [0.0, np.pi, -np.pi, -np.pi]
    expectedResults = [0.0, 0.0, 0.0, 0.0]
    actualResults = [1.0, 2.0, 3.0, 4.0]
    for i, n in enumerate(angleSim):
        actualResults[i] = deltaAngle(angleSim[i], angleSun[i])
    if actualResults != expectedResults:
        print(actualResults)
        print('something went wrong')
        return False
    print("Done")
    return True

def testincidentPower():
    print("Testing incidentPower...")
    sunTestAngles1 = [0.0, np.pi, np.pi/2.0, np.pi/4.0]
    sunTestAngles2 = [0.0, np.pi, np.pi/2.0, np.pi/3.0]
    simTestAngles1 = [0.0, 0.0, np.pi, np.pi/5.0]
    simTestAngles2 = [0.0, 0.0, np.pi, np.pi/23.0]
    expectedResults = [0.0, 0.0, 500.0, 61.782]
    actualResults = [0.0, 0.0, 2500.0, 0.0]
    print("Charge rate: ", chargeRate)
    for i, n in enumerate(expectedResults):
        actualResults[i] = getEnergyGenerated(simTestAngles1[i], simTestAngles2[i], sunTestAngles1[i], sunTestAngles2[i])
    if actualResults != expectedResults:
        print(actualResults)
        print('something went wrong')
        return False
    print("Done")
    return True

def runTests():
    if not testcheckAngle():
        print("checkAngle function failed")
        return
    
    if not testdeltaAngle():
        print("deltaAngle function failed")
        return
    
    if not testincidentPower():
        print('incidentPower function failed')
        return
    
    print("All functions worked")
    return

def main():
    #runTests()
    pass

if __name__ == "__main__":
    main()

