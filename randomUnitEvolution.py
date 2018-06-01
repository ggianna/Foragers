import random
import copy
from runGame import Game
from output import Output
from economy import Economy
from gamemap import GameMap



class RandomUnitEvolution():
    def __init__(self):
        pass

    def evolveEachUnit(self, economy,  gameMap,  army):
        output = Output() # Dummy output
        newArmy = copy.deepcopy(army)

        # For each unit
        for unitIdx in range(len(newArmy)):
            # Get the i-th unit of the army
            unitToOptimize = newArmy[unitIdx]


            bestUnit = copy.deepcopy(unitToOptimize)
            bestScore = 0
            for i in range(1, 100):
                # Create an instance of our army, based on the original army, which we will use in a given game
                fodderArmy = copy.deepcopy(newArmy)
                # Create a (changeable) map, based on the original map
                changeableMap = copy.deepcopy(gameMap)

                # create a "trained"/improved version of the unit we optimize, on the changeable map
                alteredUnit = self.getImprovedClone(unitToOptimize, changeableMap)
                # Update the fodder army with the altered unit
                fodderArmy[unitIdx] = alteredUnit
                self.updateArmyWithCurrentMap(fodderArmy, changeableMap);

                # We create a new game, with the changeable map
                g = Game(economy,  changeableMap,  fodderArmy,  output, 0.0);
                score = self.runGame(g)
                if score > bestScore:
                    bestScore = score
                    bestUnit = alteredUnit

                print ("Run %d"%(i))
            # Update the army
            newArmy[unitIdx] = bestUnit

    def updateArmyWithCurrentMap(self, fodderArmy, newMap):
        for unit in fodderArmy:
            unit.setMap(newMap)
        return fodderArmy


    def runGame(self, game):
        evaluationScore = game.run();
        return evaluationScore;

    def getImprovedClone(self, unit, mapToAssign):
        randomNumber = random.random();
        # Creates a copy of the unit
        resUnit = copy.deepcopy(unit)
        # Update traits
        resUnit.strategy.curiosity = randomNumber
        # Update map
        resUnit.setMap(mapToAssign)
        return resUnit

def main():
    economy = Economy()
    output = Output()
    curmap = GameMap(economy)
    myevol = RandomUnitEvolution()
    myevol.evolveEachUnit(economy, curmap, Game.selectArmy(economy, curmap, "white", output))

if __name__ == '__main__':
    main()
