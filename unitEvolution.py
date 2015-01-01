#!/usr/bin/python
from pygene.gene import FloatGene
#from pygene.organism import GenomeSplitOrganism
from pygene.organism import Organism
from pygene.population import Population
from runGame import Game;
from economy import Economy;
from soldiers import *;
import gamemap;
from output import Output, ConsoleOutput;

from multiprocessing import Pool
import numpy
import time

from foragers import App

class ProbGene(FloatGene):
    """
    Gene which represents the numbers used in our organism
    """
    # genes get randomly generated within this range
    randMin = 0.00
    randMax = 1.00
    
    # probability of mutation
    mutProb = 0.10
    
    # degree of mutation
    mutAmt = 0.10
    
def runGame(g):
  return g.run()

class SoldierOrganism(Organism):
    """
    Implements the organism which tries
    to survive in a game
    """
    genome = {'riskinessSoldierClass':ProbGene, 'riskinessTrapClass':ProbGene, 
      'riskinessTowerClass': ProbGene,  'curiosity':ProbGene,  'groupSpirit':ProbGene, 
      'fasting':ProbGene,  'greed':ProbGene,  'spontaneity':ProbGene, 'repetition':ProbGene};
    economy = None
    gameMap = None

    def __init__(self, **kw):
      try:
        #print "Loading soldier class"
        SoldierOrganism.soldierClass = kw.get("soldierClass")
        del kw["soldierClass"]
        #print "Done"
      except:
        print "Reverting to default class since no class was given for soldier organism."
        SoldierOrganism.soldierClass = "SoldierClass"
      super(SoldierOrganism, self).__init__(**self.genome)

    
    def getGameMap(self, bReset = False):
      if self.gameMap is None or bReset:
        economy = self.getEconomy();
	self.gameMap = gamemap.GameMap(economy, 10, 10);
      return self.gameMap
    
    def getEconomy(self, bReset = False):
      if self.economy is None or bReset:
        self.economy = Economy(5000);
      return self.economy

    
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
  
    # TODO: To use???
    def loadFromSoldier(self, sSoldier):
      self['riskinessSoldierClass'] = sSoldier.riskiness["SoldierClass"]
      self['riskinessTrapClass'] = sSoldier.riskiness["TrapClass"]
      self['riskinessTowerClass'] = sSoldier.riskiness["TowerClass"];
      self['curiosity'] = sSoldier.curiosity
      self['groupSpirit'] = sSoldier.groupSpirit
      self['fasting'] = sSoldier.fasting
      self['greed'] = sSoldier.greed
      self['spontaneity'] = sSoldier.spontaneity
      self['repetition'] = sSoldier.repetition
      
      return self;

      
    def getHelper(self,  economy,  gameMap):
      s = SoldierClass(economy,  gameMap);
      return s;
      
    # submit fitness calculation to worker process
    def prepare_fitness(self):
        self.NUMBER_OF_GAMES = 20;
        self.NUMBER_OF_SOLDIERS = 1;
        self.NUMBER_OF_HELPERS = 3;
        self.results = []
        
        for iGameCnt in range(self.NUMBER_OF_GAMES):
          # Init messaging
          output = Output();
          # Init  army
          # Set colors
          sAttackerColor = "white";
          # Init economy and map
          economy = self.getEconomy(False);
          gameMap = self.getGameMap(True);
          # Get army
          army = [self.getSoldier(economy,  gameMap) for x in range(self.NUMBER_OF_SOLDIERS)];
          army += [self.getHelper(economy,  gameMap) for x in range(self.NUMBER_OF_HELPERS)];
            
          for curSoldier in army: curSoldier.color = sAttackerColor;
          # Init game
          g = Game(economy,  gameMap,  army,  output,  0.0);    
          self.results.append(pool.apply_async(runGame, [g]))
    
    # DEBUG LINES
    #print len(self.results)
      
    def fitness(self):
        """
        Implements the 'fitness function' for this species.
        Organisms try to evolve to minimise this function's value
        """
        
        try:
          return self.cachedFitness
        except:
          pass
          
        scores = [];
        for curRes in self.results:
          scores += [float(curRes.get())]
        # DEBUG LINES
        #print curRes.get()
        # DEBUG LINES
        #raw_input()
        
        # Save avg score
        self.avgScore = numpy.percentile(scores, 0.33);
    
        # Init economy and map
        economy = self.getEconomy(False);
        gameMap = self.getGameMap(True);
        basePrice = self.NUMBER_OF_SOLDIERS * self.getEconomy(False).cost(self.getSoldier(economy,  gameMap));
        # Calc evaluation (lower is better)
        self.cachedFitness = (1000.0 + 5.0 * basePrice) / (self.avgScore + 1.0)
        return self.cachedFitness;

    def __repr__(self):
        sPhenotype = ";".join([x + ":" + ("%5.3f"%(self[x])) for x in self.genome.keys()]);
        return "%s <fitness=%4.2f (or score %4.2f)> %s" % (self.soldierClass,
            self.fitness(),  self.avgScore, 
            sPhenotype
            )


class SoldierPopulation(Population):
  
    def __init__(self, *a, **kw):
      # DEBUG LINES
      #print str(kw.get("species"))
      
      super(SoldierPopulation, self).__init__(species=kw.get("species"))
      #print "Done"
      
      
    initPopulation = 10
    #species = SoldierOrganism
    
    # cull to this many children after each generation
    childCull = 10

    # number of children to create after each generation
    childCount = 10

    # number of random new orgs to add each generation, default 0 
    numNewOrganisms = 10


def runEvolutionFor(sSoldier):
  # Globals
  global pool
  pool = Pool(processes=4)
  sSoldierType = type(sSoldier).__name__
  sSoldier
  
  # Create custom organism
  class cLocalOrganism(SoldierOrganism):
    def __init__(self, **kw):
      super(cLocalOrganism, self).__init__(soldierClass=sSoldierType, **kw);
      
  pop = SoldierPopulation((),species=cLocalOrganism)
  #pop.setSpecies('localOrganism')
  
  # create a new population, with randomly created members        
  maxGens = 10;

  import time
  lastTime = time.time()
  
  try:
      generations = 0
      while True:
  
	  # execute a generation
	  pop.gen()
	  generations += 1

	  # and dump it out
	  #print [("%.2f %.2f" % (o['x1'], o['x2'])) for o in pop.organisms]
	  best = pop.organisms[0]
	  # DEBUG LINES
	  print("Fitness %4.2f (%s)" % (best.get_fitness(), str(best)))
	  print "Generation running time %d secs"%(time.time() - lastTime)
	  lastTime = time.time()
	  if best.get_fitness() < 0.10 or generations >= maxGens:
	      break


  except KeyboardInterrupt:
      pass
  print("Executed", generations, "generations")
  print("on species ", str(pop.species.soldierClass))
  print("best soldier ", str(best.getSoldier(None, None)))
  print("with genome ",str(best))


# now a func to run the population
def main():
    # Globals
    global pool
    pool = Pool(processes=4)
    
    # Init calculator pool
    sSoldierClass = 'BarbarianClass'
    
    print "Starting run for " + sSoldierClass

    # Create custom organism
    class cLocalOrganism(SoldierOrganism):
      def __init__(self, **kw):
        super(cLocalOrganism, self).__init__(soldierClass='BarbarianClass', **kw)
      
    pop = SoldierPopulation((),species=cLocalOrganism)
    #pop.setSpecies('localOrganism')
    
    # create a new population, with randomly created members        
    maxGens = 10;

    lastTime = time.time()
    
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
            print "Generation running time %d secs"%(time.time() - lastTime)
            lastTime = time.time()
            if best.get_fitness() < 0.10 or generations >= maxGens:
                break


    except KeyboardInterrupt:
        pass
    print("Executed", generations, "generations")
    print("on species ", str(pop.species.soldierClass))
    print("best soldier ", str(best.getSoldier(None, None)))
    print("with genome ",str(best))

    print "Running emulation..."
    # Init economy and map
    economy = best.getEconomy(False);
    gameMap = best.getGameMap(True);
    output = ConsoleOutput();
    # Get army
    army = [best.getSoldier(economy,  gameMap) for x in range(best.NUMBER_OF_SOLDIERS)];
    army += [best.getHelper(economy,  gameMap) for x in range(best.NUMBER_OF_HELPERS)];
      
    # Set colors
    sAttackerColor = (255, 255, 255);
    for curSoldier in army: curSoldier.color = sAttackerColor;
    # Init game
    #g = Game(economy,  gameMap,  army,  output,  0.1);    
    output = Output() # Redirect to NULL output
    theApp = App(economy,  gameMap, army, output)
    theApp.on_execute()
    
    resScore = theApp.finalScore
    
    print "Final score:" + str(resScore)
    print "Expected:" + str(best)
    output.saveToFile("logBest.txt")
    

if __name__ == '__main__':
    main()
