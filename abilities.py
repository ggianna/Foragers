import soldiers;
import towers;

class Ability(object):
  def __init__(self, owner):
    self.targetType = None;
    self.group = "foes"; # friends/foes/traps
    self.frequency = "battle"; # battle/constant/# for uses/0.# for probability
    self.owner = owner;
    
  def applyTo(self, target, friends, foes,  traps=[]):
    if (not self.isApplicable(target, friends, foes,  traps)):
      # DEBUG LINES
      #print "Not applicable to " + type(target).__name__ + " in " +\
    #self.group + " group.";
      return None; # Indicate problem
    
    #print "Applying " + type(self).__name__ + " to " +\
      #str(target) + ".";
    return target;
  
  def isApplicable(self, target, friends, foes,  traps=[]):
    # DEBUG LINES
    #print "Self.group:" + str(eval(self.group));
    return isinstance(target, self.targetType) and (target in eval(self.group));
  
  def __str__(self):
    try:
      return self.msg;
    except:
      return object.__str__(self);

  
class Heal(Ability):
  
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType =soldiers.SoldierClass;
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, friends, foes);
    if (target == None):
      return target;
    
    target.currentHp += 0.10 * target.hp;
    
    return target;

class Harm(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = soldiers.SoldierClass;
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.currentHp -= 0.10 * target.hp;
    self.msg = "* %s HARMS %s, who now has %d hp remaining."%(str(self.owner), str(target), target.currentHp);
    
    return target;
  
class Haste(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType =soldiers.SoldierClass;
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.attackSpeed *= 2.0;
    
    return target;
  
class Slow(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType =soldiers.SoldierClass;
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.attackSpeed /= 2.0;
    self.msg = "* %s SLOWS %s, who now has %d attacks per minute."%(str(self.owner), str(target), target.attackSpeed);
    
    return target;
  
class DustToDust(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = towers.TowerClass;
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.currentHp /= 10.0;
    self.msg = "* %s casts DUST TO DUST on %s, which now has %d hp remaining."%(str(self.owner), str(target), target.currentHp);
    
    return target;
  
class BowAttack(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = soldiers.SoldierClass;    
    self.frequency = "2";
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.currentHp -= max(0.1 * self.owner.attack,  1);
    self.msg = "* %s attacks %s with a BOW, leaving the latter with %d hp."%(str(self.owner), str(target), target.currentHp);
    
    return target;

class DaggerThrownAttack(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = soldiers.SoldierClass;    
    self.frequency = "5";
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.currentHp -= max(0.05 * self.owner.attack,  1);
    self.msg = "* %s THROWS A DAGGER to %s, leaving the latter with %d hp."%(str(self.owner), str(target), target.currentHp);
    
    return target;

class CriticalAttack(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = soldiers.SoldierClass;    
    self.frequency = "0.1";
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.currentHp -= max(self.owner.attack,  1);
    self.msg = "* %s causes a CRITICAL HIT to %s, leaving the latter with %d hp."%(str(self.owner), str(target), target.currentHp);
    
    return target;

class CharmFoe(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = soldiers.SoldierClass;    
    self.frequency = "0.05";
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    foes.remove(target);
    friends.append(target);
    
    self.msg = "* %s CHARMS %s, who now changes sides!"%(str(self.owner), str(target));
    
    return target;

class Rage(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = soldiers.SoldierClass;    
    self.frequency = "constant";
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    self.owner.defence /= 1.0 + (self.owner.hp - self.owner.currentHp) / (5 * self.owner.hp);
    self.owner.attack *= 1.0 + (self.owner.hp - self.owner.currentHp ) / (5 * self.owner.hp);
    
    self.msg = "* %s is enraged! Defense is increased. Now defence is %4.2f and attack is %4.2f."%(str(self.owner), self.owner.defence, self.owner.attack);
    
    return target;

class Exhaust(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = soldiers.SoldierClass;    
    self.frequency = "0.10";
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.fullness -= 10;
    self.msg = "* %s EXHAUSTS %s. Now fullness of the latter is %4.2f."%(str(self.owner), str(target), target.fullness);
    
    return target;

class Poison(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = soldiers.SoldierClass;    
    self.frequency = "0.20";
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
  
    target.attack *= 0.9;
    target.attackSpeed *= 0.9;
    target.defence *= 0.9;
    
    self.msg = "* %s POISONS %s. Now attack, defence and speed of the latter are reduced."%(str(self.owner), str(target));
    
    return target;

class Disease(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = soldiers.SoldierClass;    
    self.frequency = "0.20";
    
  def applyTo(self, target, friends, foes,  traps=[]):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
  
    target.vulnerabilities += ['physical'];
    
    self.msg = "* %s causes DISEASE to %s. Now the target is vulnerable to physical attacks."%(str(self.owner), str(target));
    
    return target;

from traps import *;

class MapLabyrinth(Ability):
    def __init__(self, owner):
      Ability.__init__(self, owner);
      self.targetType = Labyrinth;
      self.group = "traps";
      self.frequency = "0.90";
    
    def applyTo(self, target, friends, foes,  traps):
      target = Ability.applyTo(self, target, friends, foes);
      if (target == None):
        return None;
    
      target.hp = 0;
      
      self.msg = "* %s MAPS %s, rendering it useless."%(str(self.owner), str(target));
      
      return target;
      
class DisarmTrap(Ability):
    def __init__(self, owner):
      Ability.__init__(self, owner);
      self.targetType = ArrowSlit;
      self.group = "traps";
      self.frequency = "0.90";
    
    def applyTo(self, target, friends, foes,  traps):
      target = Ability.applyTo(self, target, friends, foes,  traps);
      if (target == None):
        return None;
    
      target.hp = 0;
      
      self.msg = "* %s DISABLES %s, rendering it useless."%(str(self.owner), str(target));
      
      return target;
  
class BridgeGap(Ability):
    def __init__(self, owner):
      Ability.__init__(self, owner);
      self.targetType = Pit;
      self.group = "traps";
      self.frequency = "0.90";
    
    def applyTo(self, target, friends, foes,  traps):
      target = Ability.applyTo(self, target, friends, foes,  traps);
      if (target == None):
        return None;
    
      target.hp = 0;
      
      self.msg = "* %s COVERS %s, rendering it useless."%(str(self.owner), str(target));
      
      return target;
  
