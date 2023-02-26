import seaborn as sb
import random
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import sys

# Experiment Controls
experimentIterations = 2000
maxDoorVal = 100

class Door:
    def __init__(self, isSelected, hasPrize):
        self.isSelected = isSelected
        self.hasPrize = hasPrize
        self.isOpened = False

class DataPoint:
    def __init__(self, doors, experimentWonNoSwitchCnt, experimentWonSwitchCnt):
        self.doors = doors
        self.experimentWonNoSwitchCnt = experimentWonNoSwitchCnt 
        self.experimentWonSwitchCnt = experimentWonSwitchCnt

def RunExperiment(doorAmt: int, switchSelection: bool):

    # Init doors, mark one as selected and one as having prize
    doors = np.array([], dtype=Door)
    selectedIndex = random.randint(0, doorAmt - 1)
    prizeIndex = random.randint(0, doorAmt - 1)
    for i in range(0, doorAmt):
        isSelectedIndex = i == selectedIndex
        isPrizeIndex = i == prizeIndex
        door = Door(isSelectedIndex, isPrizeIndex)
        doors = np.append(doors, door)

    # Open all but one selected doors without the prize
    openDoorCnt = 0
    for door in doors:
        if(not door.isSelected and not door.hasPrize and not (openDoorCnt == doorAmt - 2)):
            door.isOpened = True
            openDoorCnt += 1

    # Determine if prize was won
    for door in doors:
        if(door.isSelected and door.hasPrize):
            if(switchSelection): return False
            else: return True
        elif(not door.isSelected and door.hasPrize):
            if(switchSelection): return True
            else: return False

# Run experiment on n doors
def GeneratePoint(doors: int):
    experimentWonNoSwitchCnt = 0
    for i in range(0, experimentIterations):
        if(RunExperiment(doors, False)):
            experimentWonNoSwitchCnt += 1

    experimentWonSwitchCnt = 0
    for i in range(0, experimentIterations):
        if(RunExperiment(doors, True)):
            experimentWonSwitchCnt += 1

    point = DataPoint(doors, experimentWonNoSwitchCnt, experimentWonSwitchCnt)
    return point

# Generate data points for doors 3 thru n
def GenerateDataset(maxDoor: int):
    points = np.array([], dtype=DataPoint)
    for i in range(3, maxDoor + 1):
        point = GeneratePoint(i)
        points = np.append(points, point)
        print(str(i) + " door experiment completed.")

    return points

# Run simulation to generate csv if applicable 
if(len(sys.argv) > 1 and sys.argv[1] == "generateData"):
    points = GenerateDataset(maxDoorVal)
    with open('points.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["# Doors", "# Wins", "Switched"])
        for point in points:
            writer.writerow([point.doors, point.experimentWonNoSwitchCnt, False])
            writer.writerow([point.doors, point.experimentWonSwitchCnt, True])

# Plot the CSV data
sb.set_theme(style="whitegrid")
dataset = pd.read_csv('points.csv')
f, ax = plt.subplots(figsize=(6.5, 6.5))
sb.despine(f, left=True, bottom=True)
sb.scatterplot(x="# Doors", y="# Wins",
                hue="Switched",
                palette="ch:r=-.2,d=.3_r",
                sizes=(1, 2), linewidth=0,
                data=dataset, ax=ax).set(title="Monty Hall Problem Simulation")

plt.axvline(x=3)
plt.show()














