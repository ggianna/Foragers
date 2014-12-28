#!/usr/bin/python
class StrategyScreen(object):
  def __init__(self, player, ui, economy):
    self.gameRound = 0
    self.ownedTerritory = 1
    self.player = player
    self.ui = ui
    self.economy = economy
    
  def __repr__(self):
    return "Round %d for Player %s. Currently owns %d regions, %d buildings and %d soldiers"%(self.gameRound,
	self.player.name, self.ownedTerritory, len(self.player.buildings), len(self.player.army))

  def show(self):
    while (true):
      print str(self)
      ui.menu({"Buildings" : self.listBuildings, "Soldiers" : self.listSoldiers,
	       "Buy new building" : self.buyBuilding, "Hire new soldier" : self.buySoldier, 
	       "Train soldiers" : self.trainSoldiers
	       })
      
  
  def listBuildings(self):
    for sBuilding in self.player.buildings:
      print str(sBuilding)


  def listSoldiers(self):
    for sBuilding in self.player.army:
      print str(sBuilding)

  def buyBuilding(self):
    for sBuilding in []:
      print str(sBuilding)

  def buySoldier(self):
    for sBuilding in self.player.army:
      print str(sBuilding)
      