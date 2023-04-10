from abc import ABC, abstractmethod

class Subsystem(ABC):

	def __init__(self):
		pass
	
	def getInput(self, userInput):
		print("User input is:" + userInput)

	def sendDisplay(self):
		return "Display words"
	
	def subsysMenu():
		pass

	@abstractmethod
	def update():
		pass

	def subsysWorking(self):
		print("Subsystem Working")

	def subsysError(self):
		print("Subsystem Error")

	def subsysCheck(self):
		print("Checking if subsystem is working")

	def powerError(self):
		print("Error with power")

	def tempError(self):
		print("Error with tempurature")





