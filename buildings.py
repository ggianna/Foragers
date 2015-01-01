class Barracks(object):
  def __init__(self):
    self.capacity = 6
    self.trainingGround = {"traps":0.0, "soldiers":0.01, "towers":0.0};
    self.mapSize = 10
    self.improvement = {"hp": 0.05, "attackSpeed": 0.05, "attack" : 0.05, "defence" : 0.05}
    self.newAbilities = []
    
  def train(self, army):
    # Keep first [capacity] soldiers to train
    armyToTrain = army[0:self.capacity]
    
    # For each army soldier
    for sCur in army:
      pass
      # TODO: implement
      # Improve army through real game
      # If roll is low enough
	# apply improvemnts
	
      

class GladiatorPit(Barracks):
  def __init__(self):
    self.capacity = 6
    self.trainingGround = {"traps":0.05, "soldiers":0.20, "towers":0.0};
    self.mapSize = 12
    self.improvement = {"hp": 0.15, "attackSpeed": 0.10, "attack" : 0.10, "defence" : 0.05}

class GladiatorSchool(Barracks):
  def __init__(self):
    self.capacity = 12
    self.trainingGround = {"traps":0.05, "soldiers":0.20, "towers":0.0};
    self.mapSize = 12
    self.improvement = {"hp": 0.20, "attackSpeed": 0.10, "attack" : 0.10, "defence" : 0.05}

class GladiatorFort(Barracks):
  def __init__(self):
    self.capacity = 12
    self.trainingGround = {"traps":0.05, "soldiers":0.20, "towers":0.0};
    self.mapSize = 15
    self.improvement = {"hp": 0.25, "attackSpeed": 0.15, "attack" : 0.15, "defence" : 0.10,
			"abilities" : 0.10}
    self.newAbilities += ["DaggerThrownAttack"]
    

class TrainingPit(Barracks):
  def __init__(self):
    self.capacity = 6
    self.trainingGround = {"traps":0.10, "soldiers":0.10, "towers":0.0};
    self.mapSize = 12
    self.improvement = {"hp": 0.10, "attackSpeed": 0.10, "attack" : 0.10, "defence" : 0.10}
    
class TrainingGround(Barracks):
  def __init__(self):
    self.capacity = 12
    self.trainingGround = {"traps":0.10, "soldiers":0.10, "towers":0.0};
    self.mapSize = 12
    self.improvement = {"hp": 0.10, "attackSpeed": 0.10, "attack" : 0.10, "defence" : 0.10, 
			"abilities" : 0.10}
    self.newAbilities += ["CriticalAttack"]
    
class TrainingFields(Barracks):
  def __init__(self):
    self.capacity = 12
    self.trainingGround = {"traps":0.10, "soldiers":0.10, "towers":0.0};
    self.mapSize = 15
    self.improvement = {"hp": 0.15, "attackSpeed": 0.15, "attack" : 0.15, "defence" : 0.15, 
			"abilities" : 0.15}
    self.newAbilities += ["CriticalAttack"]
    
class TechnicalLab(Barracks):
  def __init__(self):
    self.capacity = 6
    self.trainingGround = {"traps":0.10, "soldiers":0.10, "towers":0.0};
    self.mapSize = 10
    self.improvement = {"hp": 0.05, "attackSpeed": 0.05, "attack" : 0.05, "defence" : 0.10, 
			"abilities" : 0.15}
    self.newAbilities += ["BridgeGap", "MapLabyrinth", "DisableTrap"]

class TechnicalClass(Barracks):
  def __init__(self):
    self.capacity = 12
    self.trainingGround = {"traps":0.10, "soldiers":0.10, "towers":0.0};
    self.mapSize = 12
    self.improvement = {"hp": 0.05, "attackSpeed": 0.05, "attack" : 0.05, "defence" : 0.10, 
			"abilities" : 0.20}
    self.newAbilities += ["BridgeGap", "MapLabyrinth", "DisableTrap"]

class TechnicalSchool(Barracks):
  def __init__(self):
    self.capacity = 12
    self.trainingGround = {"traps":0.10, "soldiers":0.10, "towers":0.0};
    self.mapSize = 15
    self.improvement = {"hp": 0.10, "attackSpeed": 0.10, "attack" : 0.10, "defence" : 0.10, 
			"abilities" : 0.25}
    self.newAbilities += ["BridgeGap", "MapLabyrinth", "DisableTrap"]

class StrategyTent(Barracks):
  def __init__(self):
    self.capacity = 6
    self.trainingGround = {"traps":0.10, "soldiers":0.10, "towers":0.10};
    self.mapSize = 10  
    self.improvement = {"hp": 0.05, "attackSpeed": 0.10, "attack" : 0.10, "defence" : 0.10, 
			"abilities" : 0.15}
    self.newAbilities += ["Exhaust", "Slow"]

class StrategyClass(Barracks):
  def __init__(self):
    self.capacity = 12
    self.trainingGround = {"traps":0.10, "soldiers":0.10, "towers":0.10};
    self.mapSize = 12  
    self.improvement = {"hp": 0.05, "attackSpeed": 0.10, "attack" : 0.10, "defence" : 0.10, 
			"abilities" : 0.20}
    self.newAbilities += ["Exhaust", "Slow"]


class StrategySchool(Barracks):
  def __init__(self):
    self.capacity = 12
    self.trainingGround = {"traps":0.15, "soldiers":0.15, "towers":0.15};
    self.mapSize = 15  
    self.improvement = {"hp": 0.05, "attackSpeed": 0.15, "attack" : 0.15, "defence" : 0.15, 
			"abilities" : 0.25}
    self.newAbilities += ["Exhaust", "Slow"]

class ArcheryTarget(Barracks):
  def __init__(self):
    self.capacity = 6
    self.trainingGround = {"traps":0.00, "soldiers":0.10, "towers":0.10};
    self.mapSize = 10
    self.improvement = {"hp": 0.05, "attackSpeed": 0.15, "attack" : 0.15, "defence" : 0.05,
			"abilities" : 0.15}
    self.newAbilities += ["BowAttack"]

class ArcheryRange(Barracks):
  def __init__(self):
    self.capacity = 6
    self.trainingGround = {"traps":0.00, "soldiers":0.10, "towers":0.10};
    self.mapSize = 10
    self.improvement = {"hp": 0.05, "attackSpeed": 0.15, "attack" : 0.15, "defence" : 0.05,
			"abilities" : 0.15}
    self.newAbilities += ["BowAttack", "CriticalAttack"]

class ArcherySchool(Barracks):
  def __init__(self):
    self.capacity = 6
    self.trainingGround = {"traps":0.00, "soldiers":0.10, "towers":0.10};
    self.mapSize = 10
    self.improvement = {"hp": 0.05, "attackSpeed": 0.15, "attack" : 0.15, "defence" : 0.05}
    self.improvement = {"hp": 0.05, "attackSpeed": 0.15, "attack" : 0.15, "defence" : 0.05,
			"abilities" : 0.25}
    self.newAbilities += ["BowAttack", "CriticalAttack"]

# TODO: MageSchool