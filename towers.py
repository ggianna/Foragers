class TowerClass(object):
    def __init__(self,  economy,  gameMap):
        self.x = 0;
        self.y = 0;
        self.z = 0;
        self.hp = 1000;
        self.mp = 0;
        self.attack = 10;
        self.attackSpeed = 30;
        self.defence = 10;
        self.abilities = [];
        self.effects = [];
        self.vulnerabilities = [];
        self.resistances = [];
        self.immunities = ["mind"];
        self.damageType = "physical";

        self.currentHp = 1000;
        self.currentMp = 0;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " t ";
        if (self.currentHp < 0.5 * self.hp):
            return "_T_";
        return "|T|";

class Fort(TowerClass):
    def __init__(self,  economy,  gameMap):
        TowerClass. __init__(self,  economy,  gameMap);
        
        self.hp *= 0.7;
        self.attack *= 0.5;
        self.attackSpeed *= 1.5;
        self.damageType = "physical";

        self.currentHp = 1000;
        self.currentMp = 0;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " f ";
        if (self.currentHp < 0.5 * self.hp):
            return "_F_";
        return "|F|";
        
class IllusionistTower(TowerClass):
    def __init__(self,  economy,  gameMap):
        TowerClass. __init__(self,  economy,  gameMap);
        
        self.hp *= 0.4;
        self.attack *= 1.5;
        self.attackSpeed *= 0.5;
        self.damageType = "mind";

        self.currentHp = 1000;
        self.currentMp = 0;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " i ";
        if (self.currentHp < 0.5 * self.hp):
            return "_I_";
        return "|I|";
        
class FireElementalistTower(TowerClass):
    def __init__(self,  economy,  gameMap):
        TowerClass. __init__(self,  economy,  gameMap);
        
        self.hp *= 0.4;
        self.attack *= 1.5;
        self.attackSpeed *= 0.5;
        self.damageType = "fire";

        self.currentHp = 1000;
        self.currentMp = 0;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " e ";
        if (self.currentHp < 0.5 * self.hp):
            return "_E_";
        return "|E|";
        
        
class WaterElementalistTower(TowerClass):
    def __init__(self,  economy,  gameMap):
        TowerClass. __init__(self,  economy,  gameMap);
        
        self.hp *= 0.4;
        self.attack *= 1.5;
        self.attackSpeed *= 0.5;
        self.damageType = "cold";
        
        self.currentHp = 1000;
        self.currentMp = 0;

    def __str__(self):
        if (self.currentHp < 0.3 * self.hp):
            return " w ";
        if (self.currentHp < 0.5 * self.hp):
            return "_W_";
        return "|W|";
        
