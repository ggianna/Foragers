class Economy(object):
    def __init__(self,  startMoney = 1000.0):
        self.startMoney = startMoney
        self.baseCost = startMoney / 10
        self.maxMoney = startMoney * 10;
        
    def cost(self,  unit):
        iBaseCost = self.baseCost
        
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
        (len(trap.immunities)) + (trap.mp);
        iBaseCost += (trap.attack * trap.attackSpeed) * (1.0 + (len(trap.abilities) / 4.0));
        
        return iBaseCost;

    def buildingCost(self, building):
      return self.baseCost * building.mapSize * (1.0 + sum(map(lambda x: building.improvement[x], building.improvement))) / 5.0
    
    def trainCost(self):
      return iBaseCost / 5.0