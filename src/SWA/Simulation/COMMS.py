class COMMS(Subsystem):

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
