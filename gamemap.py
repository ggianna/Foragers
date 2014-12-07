import random;
from traps import *;
from treasures import *;

class GameMap(object):
    def getInstanceOfTrap(self,  sClassName):
      return eval(sClassName +"()");
      
    def getInstanceOfTreasure(self,  sClassName):
      return eval(sClassName +"(self.economy, self)");
    
    def __init__(self,  economy, xSize=10,  ySize=10, trapProbability=0.10, treasureProbability=0.10):
        self.economy = economy;
        self.xSize = xSize;
        self.ySize = ySize;
        self.trapProbability = trapProbability;
        self.treasureProbability = treasureProbability;
        self.homePos = (0, 0);
    
        self.traps = [];
        self.treasures = [];
        
        self.applyTraps();
        self.applyTreasures();
        
    def applyTraps(self, possibleTraps = ["TrapClass", "Pit", "ArrowSlit", "Explosion", "Labyrinth"]):
        # Apply traps
        self.traps = [];
        for iCnt in range(0,  self.xSize): 
          for iCnt2 in range(0,  self.ySize):
            if (random.random() < self.trapProbability):
              curTrap = self.getInstanceOfTrap(random.choice(possibleTraps));
              curTrap.x = iCnt;
              curTrap.y = iCnt2;
          
              self.traps.append(curTrap);
          
          
    def applyTreasures(self, possibleTreasures = ["TreasureClass", "SmallTreasure", "BigTreasure", "HugeTreasure",
                  "Ration", "SmallRation", "BigRation", "HugeRation",
                  "Chest", "SmallChest", "BigChest", "HugeChest"
                  ]):
        # Apply treasures
        for iCnt in range(0,  self.xSize): 
          for iCnt2 in range(0,  self.ySize):
            if (random.random() < self.treasureProbability):
              curTreasure = self.getInstanceOfTreasure(random.choice(possibleTreasures));
              curTreasure.x = iCnt;
              curTreasure.y = iCnt2;
          
              self.treasures.append(curTreasure);
          
    def getTraps(self, x, y):
      res = [];
      for curTrap in self.traps:
        if (curTrap.x == x and curTrap.y == y):
          res.append(curTrap);
          
      return res;
          
    def getTreasures(self, x, y):
      res = [];
      for curTreasure in self.treasures:
        if (curTreasure.x == x and curTreasure.y == y):
          res.append(curTreasure);
          
      return res;
