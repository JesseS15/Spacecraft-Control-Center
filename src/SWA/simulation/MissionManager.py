from MissionScript import MissionScript

# Dictionary to hold all the missions
AllMissions = { }


def addMission(mName):
    AllMissions[mName] = MissionScript(mName)

def removeMission(mName):
    del AllMissions[mName]
