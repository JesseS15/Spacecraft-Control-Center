
#Sending and Receiving Power ##################################################

def sendPower(requestedPower, params, subsystemName):  
    availablePower = params['available power'] - requestedPower
    expendedPower = params['expended']+ requestedPower
    powerDistributed = params['power distribution'][subsystemName] + requestedPower
    return availablePower, expendedPower, powerDistributed

def returnPower(returnedPower, params, subsystemName):  #Returning power back to the EPS 
    availablePower = params['available power'] + returnedPower
    expendedPower = params['expended power'] - returnedPower
    powerDistributed = params['power distribution'][subsystemName] - returnedPower
    return availablePower, expendedPower, powerDistributed

#Process Requests #########################################

def checkPower(requestedPower, subsystemName, params):  #Checks to see if the power requested is a valid amount that subsytem can request
    maxPower = params['simcraft power restrictions'][subsystemName]
    if maxPower < requestedPower: return False
    if params['power distribution'][subsystemName] + requestedPower < maxPower:
        return True
    else:
        return False 

def requestPower(requestedPower, params, subsystemName):
    if not checkPower(requestedPower, subsystemName, params): 
        print('Invalid request')
        return None, None, None, None
    return sendPower(requestedPower, params, subsystemName)

def main():
    pass

if __name__ == "__main__":
    main()