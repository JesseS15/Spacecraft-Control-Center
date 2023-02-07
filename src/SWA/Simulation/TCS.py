class TCS(Subsystem):

    tempRegulation = [0,1]
    tempRateOfChange = 0.0

    def regulationFunction():
        print("Function to regulate tempurature")

    def regulationError():
        print("Error with tempurature regulation in TCS")