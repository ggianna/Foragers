from abilities import *;
from unitStrategy import *;

class SoldierClass(object):
    fullness = 40;

    def __init__(self,  economy = None,  gameMap  = None):
        self.x = 0;
        self.y = 0;
        self.z = 0;
        self.hp = 100;
        self.mp = 100;
        self.attack = 10;
        self.attackSpeed = 60;
        self.defence = 10;
        self.abilities = [];
        self.effects = [];
        self.vulnerabilities = [];
        self.resistances = [];
        self.immunities = [];
        self.damageType = "physical";
        
        # TODO: Check what to do with gameMap
        if gameMap is not None:
	  self.strategy = UnitStrategyClass(economy,  self,  gameMap.homePos);
	else:
	  self.strategy = UnitStrategyClass(economy,  self,  (0,0));
        
        self.currentHp = self.hp;
        self.currentMp = self.mp;
        
        self.fullness = SoldierClass.fullness;
        self.treasure = 0;
        self.score = 0.0;
        
        self.economy = economy;
        self.gameMap = gameMap;

    def foesToAttack(self,  friends,  foes):
        res = [];
        for curFoe in foes:
            # TODO: Use "in range" approach
            if (curFoe.x == self.x and curFoe.y == self.y):
                res.append(curFoe);
        
        return res;

    def friendsNear(self,  friends,  foes):
        res = [];
        for curFriend in friends:
            # TODO: Use "in range" approach
            if (curFriend.x == self.x and curFriend.y == self.y):
                res.append(curFriend);
        
        return res;

    def act(self,  friends,  foes,  game, canMove = True):
        bActed = False
        
        lTraps = self.gameMap.getTraps(self.x,  self.y);
        lTreasures = self.gameMap.getTreasures(self.x,  self.y);
        lFoes = self.foesToAttack(friends,  foes);
        lFriends = self.friendsNear(friends,  foes);
        
        # Decide move
        if canMove:
	  mMove = self.strategy.decideMove(lFriends,  lFoes,  self.gameMap);
	  bActed = True
	else:
	  mMove = (0,0)
        # DEBUG LINES
#        game.output.log("Moving:" + str(mMove));
        ##########
        self.move(mMove);
        
        if len(lTraps) > 0:
            for curTrap in lTraps:
                # DEBUG LINES
#                game.output.log("\n\n!!! Interacted with trap %s."%(str((curTrap.x,  curTrap.y))));
                ##########
                
                if not game.interactWithTrap(self,  curTrap,  lFriends,  lFoes,  [curTrap]):
		  bActed = True
                  return bActed;
                
        if len(lFoes) > 0:
            for curFoe in lFoes:
                # DEBUG LINES
#                game.output.log("\nBattled foe!");
                ##########
                if not game.interactWithFoe(self,  curFoe,  lFriends,  lFoes):
		  bActed = True
                  return bActed;
                
        if len(lTreasures) > 0:
            for curTreasure in lTreasures:
                # DEBUG LINES
#                game.output.log("\nGot treasure %s!!!"%(str((curTreasure.x,  curTreasure.y))));
                ##########
                if not game.interactWithTreasure(self,  curTreasure,  lFriends,  lFoes):
		  bActed = True
                  return bActed;

        if self.x == self.gameMap.homePos[0] and self.y == self.gameMap.homePos[1]:
	    if not game.interactWithHome(self):
		  bActed = True
                  return bActed;

	return bActed
    
    def move(self, moveTuple):
        self.move3D(moveTuple[0], moveTuple[1], 0);
        
#    def move(self, xMove, yMove):
#        self.move3D(xMove, yMove, 0);
        
    def move3D(self, xMove, yMove, zMove):
        self.x += xMove;
        self.y += yMove;
        self.z += zMove;
        
    def doAction(self, sActionName, oTarget):
        return True;
        
    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " S ";
        if (self.currentHp < 0.5 * self.hp):
            return "_S_";
        return "/S\\";

        
class KnightClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.hp *= 1.25; # 10 percent more hitpoints
        self.damageType = "physical";
        self.attackSpeed *= 0.9;
        self.defence *= 1.10;
        self.vulnerabilities += ["mind", "fire"];
        self.resistances += ["cold"];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " K ";
        if (self.currentHp < 0.5 * self.hp):
            return "_K_";
        return "/K\\";

class BarbarianClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.hp *= 1.25; # 10 percent more hitpoints
        self.damageType = "physical";
        self.attackSpeed *= 0.9;
        self.defence *= 0.80;
        self.vulnerabilities += ["mind"];
        self.resistances += ["cold"];
        self.abilities += [Rage(self)];
        

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " B ";
        if (self.currentHp < 0.5 * self.hp):
            return "_B_";
        return "/B\\";

        
class MageClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.attack *= 1.50;
        self.hp *= 0.90;
        self.damageType = "mind";
        self.defence *= 0.80;
        self.resistances += ["mind"];
        self.abilities += [Harm(self)];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " M ";
        if (self.currentHp < 0.5 * self.hp):
            return "_M_";
        return "/M\\";

class DruidClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.attack *= 1.50;
        self.hp *= 0.90;
        self.damageType = "mind";
        self.defence *= 0.80;
        self.resistances += ["mind"];
        self.abilities += [Slow(self)];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " D ";
        if (self.currentHp < 0.5 * self.hp):
            return "_D_";
        return "/D\\";

class WizardClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.attack *= 1.80;
        self.attackSpeed *= 0.6;
        self.hp *= 0.60;
        self.damageType = "fire";
        self.defence *= 0.50;
        self.immunities += ["mind"];
        self.abilities += [Slow(self), DustToDust(self)];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " W ";
        if (self.currentHp < 0.5 * self.hp):
            return "_W_";
        return "/W\\";

class RangerClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.attack *= 1.20;
        self.attackSpeed *= 1.20;
        self.hp *= 0.90;
        self.damageType = "physical";
        self.defence *= 0.80;
        self.abilities += [BowAttack(self)];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " R ";
        if (self.currentHp < 0.5 * self.hp):
            return "_R_";
        return "/R\\";

class AssassinClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.attack *= 0.90;
        self.attackSpeed *= 1.50;
        self.hp *= 0.80;
        self.damageType = "physical";
        self.defence *= 0.70;
        self.abilities += [DaggerThrownAttack(self),  CriticalAttack(self)];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " X ";
        if (self.currentHp < 0.5 * self.hp):
            return "_X_";
        return "/X\\";

class EnchanterClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.attack *= 0.50;
        self.attackSpeed *= 0.70;
        self.hp *= 0.80;
        self.damageType = "mind";
        self.defence *= 0.70;
        self.abilities += [CharmFoe(self)];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " E ";
        if (self.currentHp < 0.5 * self.hp):
            return "_E_";
        return "/E\\";

class TechnicianClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.attack *= 0.50;
        self.attackSpeed *= 0.70;
        self.hp *= 0.80;
        self.damageType = "physical";
        self.defence *= 0.70;
        self.abilities += [DisarmTrap(self)];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " t ";
        if (self.currentHp < 0.5 * self.hp):
            return "_t_";
        return "/t\\";

class CartographerClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.attack *= 0.50;
        self.attackSpeed *= 0.70;
        self.hp *= 0.80;
        self.damageType = "physical";
        self.defence *= 0.70;
        self.abilities += [MapLabyrinth(self)];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " c ";
        if (self.currentHp < 0.5 * self.hp):
            return "_c_";
        return "/c\\";

class BridgeBuilderClass(SoldierClass):
    def __init__(self,  economy,  gameMap):
        SoldierClass.__init__(self, economy, gameMap);
        
        self.attack *= 0.60;
        self.attackSpeed *= 0.40;
        self.hp *= 0.90;
        self.damageType = "physical";
        self.defence *= 0.60;
        self.abilities += [BridgeGap(self)];

        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " b ";
        if (self.currentHp < 0.5 * self.hp):
            return "_b_";
        return "/b\\";
