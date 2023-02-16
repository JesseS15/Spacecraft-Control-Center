
# Need to create

class Subsystem:

	isWorking = False
	isActive = False
	hasPower = False
	powerUsage = 0.0
	powerRange = [0,10]
	tempAcceptable = False
	tempValue = 0.0
	tempRange = [0,10]

	def __init__(self):
		print("New subsystem created")
	
	def subsysWorking():
		print("Subsystem Working")

	def subsysError():
		print("Subsystem Error")

	def subsysCheck():
		print("Checking if subsystem is working")

	def powerError():
		print("Error with power")

	def tempError():
		print("Error with tempurature")





