from abilities import *;

class TrapClass(object):
    def __init__(self):
        self.x = 0;
        self.y = 0;
        self.z = 0;
        self.hp = 100;
        self.mp = 0;
        self.attack = 10;
        self.attackSpeed = 1000;
        self.defence = 50;
        self.abilities = [Harm(self)];
        self.effects = [];
        self.vulnerabilities = [];
        self.resistances = [];
        self.immunities = ["mind"];
        self.damageType = "physical";

        self.currentHp = 1000;
        self.currentMp = 0;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " _ ";
        if (self.currentHp < 0.5 * self.hp):
            return " ~ ";
        return " # ";

class Pit(TrapClass):
    def __init__(self):
      TrapClass.__init__(self);
      
      self.abilities = [Harm(self), Slow(self)];

    def __str__(self):
        return "\\_/";

class ArrowSlit(TrapClass):
    def __init__(self):
      TrapClass.__init__(self);
      
      self.abilities = [Poison(self)];

    def __str__(self):
        return "-^-";


class Explosion(TrapClass):
    def __init__(self):
      TrapClass.__init__(self);
      self.attackSpeed = 120;
      self.attack = 5;
      self.damageType = "fire";
      
      self.abilities = [Harm(self)];

    def __str__(self):
        return "-^-";

class Labyrinth(TrapClass):
    def __init__(self):
      TrapClass.__init__(self);
      self.attackSpeed = 120;
      self.attack = 2;
      self.damageType = "mind";
      
      self.abilities = [Exhaust(self)];


    def __str__(self):
        return "-@-";
