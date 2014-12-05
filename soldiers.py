from abilities import *;

class SoldierClass(object):
    def __init__(self):
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
        
        self.currentHp = self.hp;
        self.currentMp = self.mp;

    def move(self, xMove, yMove):
        self.move3D(xMove, yMove, 0);
        
    def move3D(self, xMove, yMove, zMove):
        self.x += xMove;
        self.y += yMove;
        self.z += zMove;
        
    def doAction(self, sActionName, oTarget):
        return True;
        
    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " s ";
        if (self.currentHp < 0.5 * self.hp):
            return "_s_";
        return "/S\\";

        
class KnightClass(SoldierClass):
    def __init__(self):
        SoldierClass.__init__(self);
        
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
            return " k ";
        if (self.currentHp < 0.5 * self.hp):
            return "_k_";
        return "/K\\";

class BarbarianClass(SoldierClass):
    def __init__(self):
        SoldierClass.__init__(self);
        
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
    def __init__(self):
        SoldierClass.__init__(self);
        
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
            return " m ";
        if (self.currentHp < 0.5 * self.hp):
            return "_M_";
        return "/M\\";

class DruidClass(SoldierClass):
    def __init__(self):
        SoldierClass.__init__(self);
        
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
            return " d ";
        if (self.currentHp < 0.5 * self.hp):
            return "_D_";
        return "/D\\";

class ArchmageClass(SoldierClass):
    def __init__(self):
        SoldierClass.__init__(self);
        
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
            return " a ";
        if (self.currentHp < 0.5 * self.hp):
            return "_A_";
        return "/A\\";

class RangerClass(SoldierClass):
    def __init__(self):
        SoldierClass.__init__(self);
        
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
            return " r ";
        if (self.currentHp < 0.5 * self.hp):
            return "_R_";
        return "/R\\";

class AssassinClass(SoldierClass):
    def __init__(self):
        SoldierClass.__init__(self);
        
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
            return " x ";
        if (self.currentHp < 0.5 * self.hp):
            return "_X_";
        return "/X\\";

class EnchanterClass(SoldierClass):
    def __init__(self):
        SoldierClass.__init__(self);
        
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
            return " e ";
        if (self.currentHp < 0.5 * self.hp):
            return "_E_";
        return "/E\\";

