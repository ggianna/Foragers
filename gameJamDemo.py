#!/usr/bin/python
import random
import copy
from runGame import Game
from output import Output
from economy import Economy
from gamemap import GameMap


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

    return score




def main():
    ### Demonstrate map generation
    # Init economy
    economy = Economy(500);
    # Init messaging
    output = Output();
    # Set colors
    sAttackerColor = "white";

    gameMap = GameMap(economy, 10, 10, 0.1, 0.1, 0.05, 0.05);
    # Create an army
    army = Game.selectArmy(economy, gameMap, "white", output)

    # For this army, create 3 maps (1 easy, 1 average, 1 difficult)
    for pParams in [(0.01, 0.10, 0.01, 0.01, "easy"), (0.1, 0.10, 0.1, 0.1, "medium"),
                    (0.2, 0.10, 0.2, 0.2, "difficult")]:
        gameMap = GameMap(economy, 10, 10, pParams[0], pParams[1], pParams[2], pParams[3]);
        # Run the easy 10 times
        allScores = []
        for iCnt in range(10):
            score = runGameMap(economy, gameMap, army, output)
            allScores += [score]

        print str(pParams) + ":" + str(allScores)
    # Record the avg performance and stdev

    # Compare the two
    # Show them

    ### Demonstrate agent training
    # Create a map
    # Select an army

    # Run game on map 10 times
    # Record avg performance
    # Evolve army
    # Run game on map 10 times
    # Record avg performance

    # Compare the two
    # Show them


if __name__ == '__main__':
    main()
