#!/usr/bin/python
from player import Player
import cPickle
from ui import UI
from economy import Economy
from training import TrainingSession
from soldiers import *
from buildings import Barracks
import os


class SinglePlayerGame:
  gameStates = ['strategy', 'foraging', 'scoreScreen']

  allowedBuildings = """Barracks
      GladiatorPit
      GladiatorSchool
      GladiatorFort
      TrainingPit
      TrainingGround
      TrainingFields
      TechnicalLab
      TechnicalClass
      TechnicalSchool
      StrategyTent
      StrategyClass
      StrategySchool
      ArcheryTarget
      ArcheryRange
      ArcherySchool""".split()
  allowedSoldiers = """SoldierClass
	KnightClass
	BarbarianClass
	MageClass
	DruidClass
	WizardClass
	RangerClass
	AssassinClass
	EnchanterClass
	TechnicianClass
	CartographerClass
	BridgeBuilderClass""".split()
	
  def __init__(self):
    sPlayerName = raw_input("Enter your name:")
    self.conqueredLands = 0;
    self.economy = Economy(5000)
    self.player = Player(sPlayerName, 5000, [SoldierClass(self.economy)] * 10, [Barracks()])
    
  def saveToFile(self, sFilename):
    print "Saving..."
    cPickle.dump( self, open( "save.p", "wb" ) )
    print "Saving... Done."

  def loadFromFile(self, sFilename):
    print "Loading..."
    self = cPickle.load( open( "save.p", "rb" ) )
    print "Loading... Done."
    
  
  def listCurrentBuildings(self):
    sRes = "Number of buildings: %d\n"%(len(self.player.buildings))
    sRes = "\n".join(map(str, self.player.buildings))
    return sRes
  
  def selectBuildingType(self, buildingList = None):
    if buildingList == None:
      buildingList = SinglePlayerGame.allowedBuildings
      
    mOpts = map(lambda x: (x, x), buildingList)    
    mOpts +=[("Cancel", lambda:  None)]
    return self.ui.menu(mOpts)
  
  def selectBuilding(self, buildingList):
    mOpts = map(lambda x: (str(x), x), buildingList)    
    mOpts +=[("Cancel", lambda:  None)]
    return self.ui.menu(mOpts)
  
  def listCurrentSoldiers(self):
    sRes = "Number of units: %d\n"%(len(self.player.army))
    sRes += "\n".join(map(str, self.player.army))
    return sRes
  
  def selectSoldier(self, soldierList = None):
    if soldierList == None:
      soldierList = SinglePlayerGame.allowedSoldiers
      
    mOpts = map(lambda x: (x, x), soldierList)
    mOpts +=[("Cancel", lambda:  None)]
    return self.ui.menu(mOpts)
  
  # Buy building
  def buyBuilding(self):
    sSelected = self.selectBuilding()
    if sSelected == None:
      return False
    bBuilding = eval(sSelected + "()")
    if not self.player.buyBuilding(self.economy, bBuilding):
      print "Not enough money..."
      return False
    
    print "Successfully bought %s!"%(str(bBuilding))
    return True;

  # Buy Army
  def buySoldier(self):
    sSelected = self.selectSoldier()
    if sSelected == None:
      return False
    bArmy = eval(sSelected + "(self.economy)")
    if not self.player.buyArmy(self.economy, bArmy):
      print "Not enough money to buy army..."
      return False
    
    print "Successfully bought %s!"%(str(bArmy))
    return True;

  # Train soldiers
  def trainSoldiers(self):
    # Select building
    sSelectedBuilding = self.selectBuilding(map(lambda x: str(x), self.player.buildings))
    if sSelectedBuilding == None:
      return

    # Put soldiers
    tTrainingSession = TrainingSession(self.economy, self.player.army, sSelectedBuilding)
    tTrainingSession.train()
    
    return True;
    

  def start(self):
    self.curState = 'strategy'
    ui = self.ui = UI()
    while True:
      os.system('clear')
      print "Player %s\nMoney: %4.2f\nArmy size: %d\nBuilding count: %d"%(self.player.name, self.player.money, len(self.player.army), len(self.player.buildings))
      
      print "Menu:"
      print "====="
      if self.curState == "strategy":
	dOpts = [("List buildings", self.listCurrentBuildings),
	  ("List army", self.listCurrentSoldiers),
	  ("Buy building", self.buyBuilding),
	  ("Buy soldier", self.buySoldier),
	  ("Train soldiers", self.trainSoldiers),
	  ("Quit", lambda : None)]
	
	# DEBUG LINES
	#print str(dOpts)
	
	sRes = ui.menu(dOpts)
	if sRes == None:
	  return
	else:
	  print sRes
	  print "Press [ENTER] to continue"
	  raw_input()
      

if __name__ == "__main__":
  g = SinglePlayerGame()
  g.start()