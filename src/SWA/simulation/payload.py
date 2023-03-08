from Simulation.Subsystem import Subsystem

class payload(Subsystem):

    payloadName = "Payload"

    def __init__(self, payloadName):
        super().__init__()
        self.payloadName = payloadName

    def payloadAction(self):
        print("Payload acction")

    
