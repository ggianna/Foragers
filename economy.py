class Economy(object):
    def __init__(self,  maxMoney = 1000.0):
        self.maxMoney = maxMoney;
        
    def cost(self,  item):
        iBaseCost = 100;
        
        iBaseCost += (item.hp * item.defence) * (1.0 + \
        (len(item.resistances) / 4.0) - (len(item.vulnerabilities) / 4.0)) * \
        (len(item.immunities)) + (item.mp);
        iBaseCost += (item.attack * item.attackSpeed) * (1.0 + (len(item.abilities) / 4.0));
        
        return iBaseCost;
