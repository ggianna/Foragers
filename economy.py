class Economy(object):
    def __init__(self,  maxMoney = 1000.0):
        self.maxMoney = maxMoney;
        
    def cost(self,  unit):
        iBaseCost = 100;
        
        iBaseCost += (unit.hp * unit.defence) * (1.0 + \
        (len(unit.resistances) / 4.0) - (len(unit.vulnerabilities) / 4.0)) * \
        (len(unit.immunities)) + (unit.mp);
        iBaseCost += (unit.attack * unit.attackSpeed) * (1.0 + (len(unit.abilities) / 4.0));
        
        return iBaseCost;

    def treasureValue(self,  treasure):
      return treasure.treasureValue + treasure.foodValue;

    def trapValue(self,  trap):
        iBaseCost = 100;
        
        iBaseCost += (trap.hp * trap.defence) * (1.0 + \
        (len(trap.resistances) / 4.0) - (len(trap.vulnerabilities) / 4.0)) * \
        (len(trap.immtrapies)) + (trap.mp);
        iBaseCost += (trap.attack * trap.attackSpeed) * (1.0 + (len(trap.abilities) / 4.0));
        
        return iBaseCost;

