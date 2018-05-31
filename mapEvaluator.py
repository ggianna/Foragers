from economy import *
from game import *

class MapEvaluator:
    def evaluate(map, listOfSoldiers):
        fitnessValue = 0.0;
        return fitnessValue;
    
    def getEasyMap(listOfSoldiers):
        pass

    def getDifficultMap(listOfSoldiers):
        pass

if __name__ == "__main__":
  # Init economy and map
  economy = Economy(50);
  gameMap = gamemap.GameMap(economy, 30, 30, 0.00, 0.10, 0.10, 0.00);  
  # Init messaging
  output = ConsoleOutput();
  # Init  army
  # Set colors
  sAttackerColor = "white";
  army = Game.selectArmy(economy,  gameMap,  sAttackerColor,  output, ['SoldierClass', 'TechnicianClass', 'MageClass']);
  
  print str(army);
        