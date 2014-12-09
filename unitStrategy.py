from math import *;
from utils import *;
import random;

class UnitStrategyClass(object):
  
  def __init__(self, economy, owner, homePos):
    self.riskiness = {"SoldierClass": 0.1, "TrapClass": 0.1, "TowerClass": 0.1}; # Base probability to get closer to interact
    self.curiosity = 0.10; # TODO: Base probability to explore new territory
    self.groupSpirit = 0.30; # Base probability to keep close to others
    self.fasting = 0.10; # Base probability to return if hungry
    self.greed = 0.90; # Base probability to reach  for loot, when not enough has been collected
    self.spontaneity = 0.05; # Base probability to act without checking/thinking
    self.repetition = 0.20;  # Base probability to get back to one's last position
    
    self.owner = owner;
    self.economy = economy;
    self.homePos = homePos;
    
    self.lastDirection = None;
  
  # Returns the offset for the unit movement
  def decideMove(self, friends, foes, gamemap):
    # Init direction scores
    directionScores = {(-1,-1): 0.0, (0, -1): 0.0, (1, -1): 0.0,
               (-1, 0): 0.0, (0, 0) : 0.0, (1, 0) : 0.0,
               (-1, 1): 0.0, (0, 1) : 0.0, (1, 1) : 0.0};
    
    lFriends = self.friendsInSight(friends, foes);
    if len(lFriends) > 0:
      # DEBUG LINES
#      print("\nFound %d friends in range.\n"%(len(lFriends) - 1));    
      
      for curFriend in friends:
        if curFriend == self.owner:
          continue; # Ignore self
        directionScores[self.directionForPosition(curFriend).tuple()] += self.groupSpirit / (len(lFriends) - 1);

    lFoes = self.foesInSight(friends, foes);
    if len(lFoes) > 0:
      # DEBUG LINES
#      print("\nFound %d foes in range.\n"%(len(lFoes)));    
      
      for curFoe in foes:
        if (curFoe is SoldierClass):
          sCurClassName = "SoldierClass";     
        if (curFoe is TowerClass):
          sCurClassName = "TowerClass";
      
        directionScores[self.directionForPosition(curFoe).tuple()] += self.riskiness[sCurClassName] / len(lFoes);
    
    lTrapsInSight = self.trapsInSight(friends, foes, gamemap);
    # DEBUG LINES
#    print("\nFound %d traps in range.\n"%(len(lTrapsInSight)));    
    
    if len(lTrapsInSight) > 0:
      for curTrap in lTrapsInSight:
        directionScores[self.directionForPosition(curTrap).tuple()] += (self.riskiness["TrapClass"]) / len(lTrapsInSight);
    
    lTreasureInSight = self.treasureInSight(friends, foes, gamemap);
    # DEBUG LINES
#    print("\nFound %d treasures in range.\n"%(len(lTreasureInSight)));    
    
    if len(lTreasureInSight) > 0:
      for curTreasure in lTreasureInSight: 
        # If not enough treasured gathered
        if (self.economy.cost(self.owner) * 1.5 - self.owner.treasure > 0):
          directionScores[self.directionForPosition(curTreasure).tuple()] += self.greed / len(lTreasureInSight);
    
    # Do we miss home because of hunger?
    if self.owner.fullness <= self.distanceFromHome():
      directionScores[self.directionForPosition(self.homePos).tuple()] += self.fasting;
      
    # Are we against going back to our last position?
    if (self.lastDirection != None):
      if (random.random() >= self.repetition):
        reverseOfLastDirection = (-self.lastDirection[0],  -self.lastDirection[1]);
        # DEBUG LINES
#        print("Reducing direction %s from %4.2f to zero."%(str(reverseOfLastDirection),  
#          directionScores[reverseOfLastDirection] ));
#        raw_input();
        
        directionScores[reverseOfLastDirection] = 0.0;
      
 
    # DEBUG LINES
#    sScores = '\n'.join([str(key)+":" + str(val) for key,  val in directionScores.iteritems()]);
#    print("\n" + sScores + "\n");
#    from time import sleep;
#    sleep(1);
#    raw_input();
    ##########
    
    # Remove negative values
    for key, val in directionScores.iteritems():
      if val < 0.0:
        directionScores[key] = 0.0;
    
    # Follow probability
    curDirection = None;
    
    # RANDOMLY select
#    curScore = random.uniform(0.0,  sum(directionScores.values()));
#    # DEBUG LINES
#    print("Rolled:" + str(curScore) + " from " + str(sum(directionScores.values())));
#    sleep(1);    
#    for curDirection in directionScores.keys():
#        curScore -= directionScores[curDirection];
#        if curScore < 0:
#          break;

    # MAX select
    curMax = -1.0;
    for curCandidate in directionScores.keys():
      if directionScores[curCandidate] > curMax:
        curDirection = curCandidate;
        curMax = directionScores[curCandidate];
    print("Max is:" + str(curMax) + " by " + str(curDirection));
#    raw_input();

    # If we are about to stay put or we are spontaneous, choose randomly
    if random.random() < self.spontaneity:
      print("Spontaneous reaction!");
#      raw_input();
      curDirection = random.choice(directionScores.keys());
      
    # If bored (same place)
    if curDirection == (0, 0):
      print("Bored! Aiming for the end of the map...");
#      raw_input();
      # aim for the end of the map
      curDirection = self.directionForPosition((gamemap.xSize,  gamemap.ySize)).tuple();

    # Check if in map limits
    if self.owner.x == gamemap.xSize - 1:
      if curDirection[0] > 0:  curDirection= (0,  curDirection[1]);
    if self.owner.y == gamemap.ySize - 1:
      if curDirection[1] > 0:  curDirection= (curDirection[0],  0);
    if self.owner.x == 0:
      if curDirection[0] < 0:  curDirection= (0,  curDirection[1]);
    if self.owner.y == 0:
      if curDirection[1] < 0:  curDirection= (curDirection[0],  0);
      
    
    # Save selected direction
    self.lastDirection = curDirection;
    
    return curDirection;

  # The list of treasures in sight
  def treasureInSight(self, friends, foes, gamemap):
    return [ curTreasure for curTreasure in gamemap.treasures if (curTreasure.x - self.owner.x < 3 and curTreasure.y - self.owner.y < 3)];
  
  # The list of treasures in sight
  def trapsInSight(self, friends, foes, gamemap):
    return [ curTrap for curTrap in gamemap.traps if (abs(curTrap.x - self.owner.x) < 3 and abs(curTrap.y - self.owner.y) < 3)];
    
  # The list of foes in sight
  def foesInSight(self, friends, foes):
    return [ curFoe for curFoe in foes if (abs(curFoe.x - self.owner.x) < 3 and abs(curFoe.y - self.owner.y) < 3)];
  
  # The list of friends in sight
  def friendsInSight(self, friends, foes):
    return [ curFriend for curFriend in friends if (abs(curFriend.x - self.owner.x) < 3 and abs(curFriend.y - self.owner.y) < 3)];
  
  # The distance from home (as Manhattan distance)
  def distanceFromHome(self):
    homePos = Point();
    homePos.x = self.homePos[0];
    homePos.y = self.homePos[1];
    
    
    return abs(self.owner.x - homePos.x) + abs(self.owner.y - homePos.y); # Manhattan distance
  
  # The movement offset that brings as closer to a position on the map
  def directionForPosition(self, pos):
    # DEBUG LINES
#    try:
#      print "Target %s at %s"%(str(pos), str((pos.x,  pos.y)));
#    except:
#      print "Target %s at %s"%(str(pos),  str((pos[0],  pos[1])));
#    print "Self at %s"%(str((self.owner.x,  self.owner.y)));
    
    try:
      x = pos[0];
      y = pos[1];
    except:
      x = pos.x;
      y = pos.y;
      
    iX = Utils.sign(x - self.owner.x );
    iY = Utils.sign(y - self.owner.y );
    res=Point();
    res.x = iX;
    res.y = iY;

    # DEBUG LINES
#    print "Proposed %s"%(str(res));
#    raw_input();
    
    return res;
  
  # Returns a score (~probability) to move towards a foe
  def moveTowardsFoe(self, foe):
    hpRatio = log(self.owner.hp / foe.hp);
    attackRatio = log(self.owner.attack / foe.attack);
    defenceRatio = log(self.owner.defence / foe.defence);
    
    # The tendency as a ratio of exponential functions
    # An value of 3 in the sum of (log) ratios is almost certainty
    # that we should move closer.
    return exp(hpRatio + attackRatio + defenceRatio) / exp(3);
 
