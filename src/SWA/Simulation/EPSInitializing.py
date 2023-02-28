import numpy as np

#Goal: Simplify the below code to be a more useful calculator

def ISSCellGenerates(): #Amount of power each cell generates on the ISS (realistic number)
    totalSolarCells = 262400
    totalElectricityGenerated = 240E3 #Number in Watts
    eachCellGenerate = totalSolarCells / totalElectricityGenerated

    totalArea = 27000   #Square feet
    eachCellArea = totalArea / totalSolarCells #Amount of space each solar cell takes
    return eachCellGenerate, eachCellArea

def totalPowerNeeded(simcraftWatts, powerRatio):
    totalPower = simcraftWatts / powerRatio
    return totalPower

def calculateCellsNeeded(totalPower, eachCellGenerates):
    cellsNeeded = np.ceil(totalPower / eachCellGenerates)
    return cellsNeeded

def calculateCellsArea(cellsNeeded, eachCellArea):
    cellArea = cellsNeeded * eachCellArea
    return cellArea

def initialize(inputWatts=200):
    simcraftWatts = inputWatts                                                  #Max power consumption of the simcraft
    powerRatio = 0.4                                                            #Percentage of generated power that is used by simcraft during charging

    eachCellGenerates, eachCellArea = ISSCellGenerates()                        #We are assuming that this simcraft is running similar specs to the ISS
    totalPower = totalPowerNeeded(simcraftWatts,powerRatio)                     #Total Power that Simcraft generates
    cellsNeeded = calculateCellsNeeded(totalPower, eachCellGenerates)           #How many cells are needed (optional)
    cellArea = calculateCellsArea(cellsNeeded, eachCellArea)                    #How many square feet of solar panels are needed (optional)

    return totalPower

def main():
    pass

if __name__ == "__main__":
    main()

