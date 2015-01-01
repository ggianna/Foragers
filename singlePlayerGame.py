#!/usr/bin/python
from player import Player
from cpickle import pickle
from ui import UI
from economy import Economy

class SinglePlayerGame:
  gameStates = ['strategy', 'foraging', 'scoreScreen']
  
  def __init__(self):
    sPlayerName = raw_input("Enter your name:")
    self.player = Player(sPlayerName, 5000, [SoldierClass] * 10, buildings=[Barracks])
    self.allowedBuildings = """Barracks
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
    self.allowedSoldiers = """SoldierClass
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
    self.conqueredLands = 0;
    self.economy = Economy(5000)
    
  def saveToFile(self, sFilename):
    print "Saving..."
    pickle.dump( self, open( "save.p", "wb" ) )
    print "Saving... Done."

  def loadFromFile(self, sFilename):
    print "Loading..."
    self = pickle.load( open( "save.p", "rb" ) )
    print "Loading... Done."
    
  
  def listCurrentBuildings(self):
    sRes = "\n".join(map(str, self.player.buildings))
    return sRes
  
  def selectBuilding(self, buildingList = self.allowedBuidings):
    mOpts = map(lambda x: (x, x), buildingList)    
    mOpts["Cancel"] = lambda:  None
    return self.ui.menu(mOpts)
  
  def listCurrentSoldiers(self):
    sRes = "\n".join(map(str, self.player.army))
    return sRes
  
  def selectSoldier(self, soldierList = self.allowedSoldiers):
    mOpts = map(lambda x: (x, x), soldierList)    
    mOpts["Cancel"] = lambda:  None
    return self.ui.menu(mOpts)
  
  # Buy building
  def buyBuilding(self, economy):
    sSelected = self.selectBuilding()
    if sSelected == None:
      return
    bBuilding = eval(sSelected + "()")
    if not self.player.buyBuilding(bBuilding):
      print "Not enough money..."
      return
    
    print "Successfully bought %s!"%(str(bBuilding))

  # Buy Army
  def buySoldiers(self):
    sSelected = self.selectSoldier()
    if sSelected == None:
      return
    bArmy = eval(sSelected + "(self.economy)")
    if not self.player.buyArmy(bArmy):
      print "Not enough money to buy army..."
      return
    
    print "Successfully bought %s!"%(str(bArmy))
    

  # Train soldiers
  def trainSoldiers(self):
    # TODO: Implement
    pass
      
    

  def start(self):
    self.curState = 'strategy'
    self.ui = UI()
    while True:
      if state == "strategy":
	# TODO: Implement
	pass
      
