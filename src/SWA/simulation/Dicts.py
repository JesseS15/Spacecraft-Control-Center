class Dicts():

	ACSDict = {
		"isWorking": False,
		"isActive": False,
		"hasPower": False,
		"powerUsage": 20.0,
		"maxPower" : 0.0,
		"powerRange": [0,10],
		"tempAcceptable": False,
		"tempValue": 0.0,
		"tempRange": [0,10],
		"altitude": 0.0,
		"orbit": 0.0,
		"roll" : 0,
        "pitch" : 0,
        "yaw" : 0
	}

	COMMSDict = {
		"isWorking": False,
		"isActive": False,
		"hasPower": False,
		"powerUsage": 20.0,
		"maxPower" : 0.0,
		"powerRange": [0,10],
		"tempAcceptable": False,
		"tempValue": 0.0,
		"tempRange": [0,10],
		"downlinkActive": False,
		"uplinkActive": False,
		"antennaWorking": False,
		"clearSignal": False
	}

	EPSDict = {
		"isWorking": False,
		"isActive": False,
		"hasPower": False,
		"powerUsage": 20.0,
		"maxPower" : 0.0,
		"powerRange": [0,10],
		"tempAcceptable": False,
		"tempValue": 0.0,
		"tempRange": [0,10],
		"powerDistribution": [0,1,2,3],
		"powerIntake": 0.0,
		"powerLevel": 0.0,
		"isChanging": False,
		"hasPowerIntake": False
	}

	TCSDict = {
		"isWorking": False,
		"isActive": False,
		"hasPower": False,
		"powerUsage": 20.0,
		"maxPower" : 0.0,
		"powerRange": [0,10],
		"tempAcceptable": False,
		"tempValue": 0.0,
		"tempRange": [0,10],
		"tempRegulation": [0,1],
		"tempRateOfChange": 0.0
	}

	finalValues = {
		"roll": 0,
		"pitch": 0,
		"yaw": 0,
		"longitude": 0
	}

	dicts = { 
		"ACS": ACSDict,
		"EPS": EPSDict,
		"COMMS": COMMSDict,
		"TCS": TCSDict
		}

	def __init__(self):
		pass