import Subsystem
class COMMS(Subsystem):

    def __init__(self) -> None:
        super().__init__()
        downlinkActive = False
        uplinkActive = False
        antennaWorking = False
        clearSignal = False

    def downlinkError():
        print("Error with the downlink")

    def uplinkError():
        print("Error with uplink")

    def antennaError():
        print("Error with antenna")

    def signalErro():
        print("Signal is not clear")
