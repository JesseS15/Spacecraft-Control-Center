import Subsystem
class EPS(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        powerDistribution = [0,1,2,3]
        powerIntake = 0.0
        powerLevel = 0.0
        isChanging = False
        hasPowerIntake = False

    def powerDistributionError():
        print("Error with power distribution")

    def powerIntakeError():
        print("Error with power intake")

    def powerLevelError():
        print("Error with power level")

