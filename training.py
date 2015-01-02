#!/usr/bin/python
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


class SoldierOrganismConverter:
  @staticmethod
  def getOrganismForSoldier(sSoldier, eEconomy):
    pass
  
  def applyGenomeToSoldier(genome, sSoldier):
    pass
  

class TrainingSession:
  def __init__(self, economy, army, building):
    self.economy = economy
    self.army = army
    self.building = building
    
    self.curGround = self.building.trainingGround
    self.curMap = gamemap.GameMap(self.building.mapSize, self.building.mapSize, curGround["traps"], 
			       curGround["treasure"], curGround["soldiers"], curGround["towers"])
  
  def train(self):
    aResArmy = []
    # For each soldier in army
    for sSoldier in self.army:
      # apply evolution
      # get organism
      # sCurOrganism = SoldierOrganismConverter.getOrganismForSoldier(sSoldier, economy)
      # call GA to evolve on map
      
      # apply training
      # for each improvement
      for sKey in self.building.improvement.keys():
	# if improvement is about abilities
	if sKey == "abilities":
	  # if roll is below threshold
	  if random.random() < self.building.improvement[sKey]:
	    # give ability
	    sSoldier.abilities = set(sSoldier.abilities) + set(random.choice(self.building.newAbilities))
	# else
	else:
	  # if roll is below threshold
	  if random.random() < self.building.improvement[sKey]:
	    # increase stat
	    eval("sSoldier." + sKey + " *= 1.05")
	
      # add to result army
      aResArmy += [SoldierOrganismConverter.applyGenomeToSoldier(sSoldier)]
      
    return aResArmy

  