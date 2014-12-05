import soldiers;
import towers;

class Ability(object):
  def __init__(self, owner):
    self.targetType = None;
    self.group = "foes"; # friends/foes
    self.frequency = "battle"; # battle/constant/# for uses/0.# for probability
    self.owner = owner;
    
  def applyTo(self, target, friends, foes):
    if (not self.isApplicable(target, friends, foes)):
      # DEBUG LINES
      #print "Not applicable to " + type(target).__name__ + " in " +\
	#self.group + " group.";
      return None; # Indicate problem
    
    #print "Applying " + type(self).__name__ + " to " +\
      #str(target) + ".";
    return target;
  
  def isApplicable(self, target, friends, foes):
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
    self.targetType = type(soldiers.SoldierClass());
    
  def applyTo(self, target, friends, foes):
    target = Ability.applyTo(self, friends, foes);
    if (target == None):
      return target;
    
    target.currentHp += 0.10 * target.hp;
    
    return target;

class Harm(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = type(soldiers.SoldierClass());
    
  def applyTo(self, target, friends, foes):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.currentHp -= 0.10 * target.hp;
    self.msg = "* %s HARMS %s, who now has %d hp remaining."%(str(self.owner), str(target), target.currentHp);
    
    return target;
  
class Haste(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = type(soldiers.SoldierClass());
    
  def applyTo(self, target, friends, foes):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.attackSpeed *= 2.0;
    
    return target;
  
class Slow(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = type(soldiers.SoldierClass());
    
  def applyTo(self, target, friends, foes):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    target.attackSpeed /= 2.0;
    self.msg = "* %s SLOWS %s, who now has %d attacks per minute."%(str(self.owner), str(target), target.attackSpeed);
    
    return target;
  
class DustToDust(Ability):
  def __init__(self, owner):
    Ability.__init__(self, owner);
    self.targetType = type(towers.TowerClass());
    
  def applyTo(self, target, friends, foes):
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
    
  def applyTo(self, target, friends, foes):
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
    
  def applyTo(self, target, friends, foes):
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
    
  def applyTo(self, target, friends, foes):
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
    
  def applyTo(self, target, friends, foes):
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
    
  def applyTo(self, target, friends, foes):
    target = Ability.applyTo(self, target, friends, foes);
    if (target == None):
      return None;
    
    self.owner.defence /= 1.0 + (self.owner.hp - self.owner.currentHp) / (5 * self.owner.hp);
    self.owner.attack *= 1.0 + (self.owner.hp - self.owner.currentHp ) / (5 * self.owner.hp);
    
    self.msg = "* %s is enraged! Defense is increased. Now defence is %4.2f and attack is %4.2f"%(str(self.owner), self.owner.defence, self.owner.attack);
    
    return target;
