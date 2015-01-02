from buildings import *
from soldiers import SoldierClass

class Player(object):
  
  def __init__(self, name, money, army, buildings):
    self.name = name
    self.money = money
    self.army = army
    self.buildings = buildings
  
  def buyArmy(self, economy, army):
    iCost = economy.cost(army)
    print "Buying army for %d coins"%(iCost)
    
    if iCost <= self.money:
      self.army += [army]
      self.money -= iCost
      return True;
    else:
      return False;
    
  def buyBuilding(self, economy, building):
    iCost = economy.buildingCost(building)
    print "Buying building for %d coins"%(iCost)
    
    if iCost <= self.money:
      self.buildings += [building]
      self.money -= iCost
      return True;
    else:
      return False;
    
    