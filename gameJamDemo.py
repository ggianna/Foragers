#!/usr/bin/python
import random
import copy
from runGame import Game
from output import *
from economy import Economy
from gamemap import GameMap
import os
from randomUnitEvolution import RandomUnitEvolution
import MapBuilder.unit_evolver


def updateArmyWithCurrentMap(fodderArmy, newMap):
    for unit in fodderArmy:
        unit.setMap(newMap)
    return fodderArmy


def runGameMap(economy, map, army, output):
    # Create an instance of our army, based on the original army, which we will use in a given game
    fodderArmy = copy.deepcopy(army)
    # Create a (changeable) map, based on the original map
    changeableMap = copy.deepcopy(map)

    updateArmyWithCurrentMap(fodderArmy, changeableMap);

    # We create a new game, with the changeable map
    g = Game(economy, changeableMap, fodderArmy, output, 0.0);
    score = g.run()
    output.saveToFile("GameTimeline.json")

    return score



def doMapGenerationComparison():
    # Init economy
    economy = Economy(500);
    # Init messaging
    output = ConsoleOutput();
    # Set colors
    sAttackerColor = "white";

    gameMap = GameMap(economy, 10, 10, 0.1, 0.1, 0.05, 0.05);
    # Create an army
    army = Game.selectArmy(economy, gameMap, "white", output)

    # For this army, create 3 maps (1 easy, 1 average, 1 difficult)
    for pParams in [(0.01, 0.15, 0.01, 0.01, "easy"), (0.05, 0.15, 0.11, 0.08, "medium"),
                    (0.03, 0.01, 0.12, 0.08, "difficult")]:
        gameMap = GameMap(economy, 10, 10, pParams[0], pParams[1], pParams[2], pParams[3]);
        # Run the easy 10 times
        allScores = []
        for iCnt in range(10):
            score = runGameMap(economy, gameMap, army, output)
            allScores += [score]

        os.rename("GameTimeline.json", "GameTimeline%s.json"%(pParams[4]))

        print str(pParams) + ":" + str(allScores)
    # Record the avg performance and stdev

    # Compare the two
    # Show them

def doAgentTrainingComparison():
    # Init economy
    economy = Economy(500);
    # Init messaging
    output = ConsoleOutput();
    # Set colors
    sAttackerColor = "white";

    # A medium map
    gameMap = GameMap(economy, 10, 10, 0.05, 0.15, 0.11, 0.08);

    # Create an army
    # Select an army
    army = Game.selectArmy(economy, gameMap, "white", output)

    # Run game on map 10 times
    allScores = []
    for iCnt in range(10):
        score = runGameMap(economy, gameMap, army, output)
        allScores += [score]

    # Record avg performance
    os.rename("GameTimeline.json", "GameTimeline%s.json" % ("Untrained"))
    print str("Scores for Untrained") + ":" + str(allScores)

    # Evolve army RANDOM
    myevol = RandomUnitEvolution()
    myevol.evolveEachUnit(economy, gameMap, army)

    # Reset scores
    allScores = []

    # Run game on map 10 times
    # Record avg performance
    for iCnt in range(10):
        score = runGameMap(economy, gameMap, army, output)
        allScores += [score]

    os.rename("GameTimeline.json", "GameTimeline%s.json" % ("TrainedRandom"))
    print str("Scores for TrainedRandom") + ":" + str(allScores)

    # Reset scores
    allScores = []

    # Evolve army GENETIC
    MapBuilder.unit_evolver.getArmy(army, gameMap, economy)

    # Run game on map 10 times
    # Record avg performance
    for iCnt in range(10):
        score = runGameMap(economy, gameMap, army, output)
        allScores += [score]

    # Record avg performance
    os.rename("GameTimeline.json", "GameTimeline%s.json" % ("TrainedGenetic"))
    print str("Scores for TrainedGenetic") + ":" + str(allScores)




def main():
    ### Demonstrate map generation
    # doMapGenerationComparison()

    ### Demonstrate agent training
    doAgentTrainingComparison()



if __name__ == '__main__':
    main()
