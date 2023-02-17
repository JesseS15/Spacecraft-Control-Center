from Subsystem import Subsystem
class TCS(Subsystem):
    #TODO THIS should be changed in the future I believe, needs to be able to handle all subsystem's temps
    def __init__(self, dicts):
        super().__init__(dicts)
        

    def regulationFunction(self):
        print("Function to regulate tempurature")

    def regulationError(self):
        print("Error with tempurature regulation in TCS")