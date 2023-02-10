from Subsystem import Subsystem
class TCS(Subsystem):
    #TODO THIS should be changed in the future I believe, needs to be able to handle all subsystem's temps
    def __init__(self) -> None:
        super().__init__()
        tempRegulation = [0,1]
        tempRateOfChange = 0.0

    def regulationFunction():
        print("Function to regulate tempurature")

    def regulationError():
        print("Error with tempurature regulation in TCS")