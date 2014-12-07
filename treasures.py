from soldiers import *;

class TreasureClass(object):
  def __init__(self, economy,  gameMap):
        self.x = 0;
        self.y = 0;
        self.z = 0;
        self.economy = economy;
        self.gameMap = gameMap;
        
        # Benefits
        self.treasureValue = economy.cost(SoldierClass(economy,  gameMap)) / 5.0;
        self.foodValue = SoldierClass(economy,  gameMap).fullness / 5.0;

  def applyEffectTo(self, target):
    target.treasure += self.treasureValue;
    target.fullness += self.foodValue;
    
  def __str__(self):
    return "*T*";

# Mixed treasure
class SmallTreasure(TreasureClass):
    def __init__(self, economy, gameMap):
        TreasureClass.__init__(self, economy,  gameMap);
        self.treasureValue /= 2.0;
        self.foodValue /= 2.0;

    def __str__(self):
        return "*t*";


    
class BigTreasure(TreasureClass):
  def __init__(self, economy, gameMap):
    TreasureClass.__init__(self, economy,  gameMap);
    self.treasureValue *= 2.0;
    self.foodValue *= 2.0;

  def __str__(self):
    return "T*T";

    

class HugeTreasure(TreasureClass):
  def __init__(self, economy, gameMap):
    TreasureClass.__init__(self, economy,  gameMap);
    self.treasureValue *= 3.0;
    self.foodValue *= 3.0;


  def __str__(self):
    return "TTT";

# Monetary only treasure

class Chest(TreasureClass):
  def __init__(self, economy, gameMap):
    TreasureClass.__init__(self, economy,  gameMap);
    self.treasureValue *= 2.0;
    self.foodValue = 0.0;

  def __str__(self):
    return "*C*";
    
class SmallChest(Chest):
  def __init__(self, economy, gameMap):
    Chest.__init__(self, economy,  gameMap);
    self.treasureValue *= 0.5;

  def __str__(self):
    return "*c*";

class BigChest(Chest):
  def __init__(self, economy, gameMap):
    Chest.__init__(self, economy,  gameMap);
    self.treasureValue *= 1.5;


  def __str__(self):
    return "C*C";
    
class HugeChest(Chest):
  def __init__(self, economy, gameMap):
    Chest.__init__(self, economy,  gameMap);
    self.treasureValue *= 2.0;

  def __str__(self):
    return "CCC";    
# Food only treasure

class Ration(TreasureClass):
  def __init__(self, economy, gameMap):
    TreasureClass.__init__(self, economy,  gameMap);
    self.treasureValue = 0.0;

  def __str__(self):
    return "*R*";

class SmallRation(Ration):
  def __init__(self, economy, gameMap):
    Ration.__init__(self, economy,  gameMap);
    self.foodValue /= 2.0;

  def __str__(self):
    return "*r*";

class BigRation(Ration):
  def __init__(self, economy, gameMap):
    Ration.__init__(self, economy,  gameMap);
    self.foodValue *= 2.0;

  def __str__(self):
    return "R*R";

class HugeRation(Ration):
  def __init__(self, economy, gameMap):
    Ration.__init__(self, economy,  gameMap);
    self.foodValue *= 3.0;


  def __str__(self):
    return "RRR";
