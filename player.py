from buildings import *

class Player(Object):
  
  def __init__(self, name, money, army = [SoldierClass, SoldierClass, SoldierClass], buildings = [Barracks]):
    self.name = name
    self.money = money
    self.army = army
    self.buildings = buildings
  
  def buyArmy(self, economy, army):
    if economy.cost(army) <= self.money:
      self.army += [army]
      self.money -= economy.cost(army)
      return True;
    else:
      return False;
    
  def buyBuilding(self, economy, building):
    if economy.cost(building) <= self.money:
      self.buildings += [building]
      self.money -= economy.cost(building)
      return True;
    else:
      return False;
    
    