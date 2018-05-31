from economy import Economy
from output import ConsoleOutput, Output
from runGame import Game
import gamemap

from deap import base
from deap import creator
from deap import tools











def EvaluateMap(chromosome = [0.00, 0.10, 0.10, 0.00] , economy = Economy(50) ):
    # Init economy and map
    economy = Economy(5000);
    gameMap = gamemap.GameMap(economy, 30, 30,  *chromosome)
    output = Output()

    armies = [ Game.selectArmy(economy, gameMap, armyColor="white", output=Output(), aUnitPool= ['SoldierClass', 'TechnicianClass', 'MageClass'])
                for _ in range(30)]
    score = sum([Game(economy, gameMap, army, output, 0.0).run() for army in armies])

    return  (score, gameMap)



if __name__ == "__main__":
  # Init economy and map
  print EvaluateMap()