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
        for unitIdx in range(len(newArmy)):
            unit = newArmy[unitIdx]

            bestUnit = copy.deepcopy(unit)
            bestScore = 0
            for i in range(1, 100):
                initialGameMap = copy.deepcopy(gameMap)
                fodderArmy = copy.deepcopy(newArmy)
                alteredUnit = self.randomizeUnit(unit)
                fodderArmy[unitIdx] = alteredUnit
                g = Game(economy,  initialGameMap,  fodderArmy,  output, 0.0);
                score = self.runGame(g)
                if score > bestScore:
                    bestScore = score
                    bestUnit = alteredUnit
            # Update the army
            newArmy[unitIdx] = bestUnit


    def runGame(self, game):
        evaluationScore = game.run();
        return evaluationScore;

    def randomizeUnit(self, unit):
        randomNumber = random.random();
        unit.strategy.curiosity = randomNumber
        return copy.deepcopy(unit)

def main():
    economy = Economy()
    output = Output()
    curmap = GameMap(economy)
    myevol = RandomUnitEvolution()
    myevol.evolveEachUnit(economy, curmap, Game.selectArmy(economy, curmap, "white", output))

if __name__ == '__main__':
    main()
