#!/usr/bin/python
from pygene.gene import FloatGene
from pygene.organism import GenomeSplitOrganism
from pygene.population import Population
from runGame import Game;
from economy import Economy;
from soldiers import *;
import gamemap;
from output import Output;

class ProbGene(FloatGene):
    """
    Gene which represents the numbers used in our organism
    """
    # genes get randomly generated within this range
    randMin = 0.00
    randMax = 1.00
    
    # probability of mutation
    mutProb = 0.05
    
    # degree of mutation
    mutAmt = 0.10

class SoldierOrganism(GenomeSplitOrganism):
    """
    Implements the organism which tries
    to survive in a game
    """
    genome = {'riskinessSoldierClass':ProbGene, 'riskinessTrapClass':ProbGene, 
      'riskinessTowerClass': ProbGene,  'curiosity':ProbGene,  'groupSpirit':ProbGene, 
      'fasting':ProbGene,  'greed':ProbGene,  'spontaneity':ProbGene, 'repetition':ProbGene};
    
    soldierClass = 'SoldierClass';
    
    def getSoldier(self,  economy,  gameMap):
      s = eval('%s(economy,  gameMap)'%(self.soldierClass));
      s.riskiness = {"SoldierClass" : self['riskinessSoldierClass'], 
        "TrapClass" : self['riskinessTrapClass'], 
        "TowerClass" : self['riskinessTowerClass'], 
        };
      s.curiosity = self['curiosity'];
      s.groupSpirit = self['groupSpirit'];
      s.fasting = self['fasting'];
      s.greed = self['greed'];
      s.spontaneity = self['spontaneity'];
      s.repetition = self['repetition'];
      
      return s;
      
    def fitness(self):
        """
        Implements the 'fitness function' for this species.
        Organisms try to evolve to minimise this function's value
        """
        
        try:
          return self.cachedFitness
        except:
          pass
          
        # Init messaging
        output = Output();
        # Init  army
        # Set colors
        sAttackerColor = "white";
        
        NUMBER_OF_GAMES = 1;
        NUMBER_OF_SOLDIERS = 5;
        avgScore = 0;
        for iGameCnt in range(NUMBER_OF_GAMES):
          # Init economy and map
          economy = Economy(5000);
          gameMap = gamemap.GameMap(economy, 20, 20);
          # Get army
          army = [self.getSoldier(economy,  gameMap) for x in range(NUMBER_OF_SOLDIERS)];
          basePrice = NUMBER_OF_SOLDIERS * economy.cost(army[0]);
          
          for curSoldier in army: curSoldier.color = sAttackerColor;
          # Init game
          g = Game(economy,  gameMap,  army,  output,  0.0);
          self.game = g;
          avgScore += self.game.run();
        avgScore /= NUMBER_OF_GAMES;
        # Save avg score
        self.avgScore = avgScore;
        # Run evaluation (lower is better)
        self.cachedFitness = (1000.0 + 5 * basePrice) / (avgScore + 1.0)
        return self.cachedFitness;

    def __repr__(self):
        sPhenotype = ";".join([x + ":" + ("%5.3f"%(self[x])) for x in self.genome.keys()]);
        return "<fitness=%4.2f (or score %4.2f)> %s" % (
            self.fitness(),  self.avgScore, 
            sPhenotype
            )

class BridgeBuilderOrganism(SoldierOrganism):
    soldierClass = 'BridgeBuilderClass';


class SoldierPopulation(Population):
    species = BridgeBuilderOrganism
    initPopulation = 10
    
    # cull to this many children after each generation
    childCull = 20

    # number of children to create after each generation
    childCount = 10

    # number of random new orgs to add each generation, default 0 
    numNewOrganisms = 10
    
# now a func to run the population
def main():
    # create a new population, with randomly created members
    pop = SoldierPopulation()
    maxGens = 20;

    try:
        generations = 0
        while True:
            # execute a generation
            pop.gen()
            generations += 1

            # and dump it out
            #print [("%.2f %.2f" % (o['x1'], o['x2'])) for o in pop.organisms]
            best = pop.organisms[0]
            print("fitness=%4.2f %s" % (best.get_fitness(), str(best)))
            if best.get_fitness() < 0.10 or generations >= maxGens:
                break

    except KeyboardInterrupt:
        pass
    print("Executed", generations, "generations")


if __name__ == '__main__':
    main()
