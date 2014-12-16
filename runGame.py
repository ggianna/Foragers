#!/usr/bin/python
from soldiers import *;
from towers import *;
from economy import Economy;
from output import ConsoleOutput;
import time;
import math;
import random;
import gamemap;
#from pprint import pformat

#import pygame;
#from pygame.locals import *;

from termcolor import colored;
#from utils import Utils;


class Game(object):
    
  # Static method definitions
  @staticmethod
  def getInstanceOf(sClassName,  economy,  gameMap):
      return eval("soldiers." + sClassName +"(economy, gameMap)");
      
  @staticmethod
  def selectArmy(eEconomy,  gameMap,  armyColor,  output,  
    aUnitPool = [
      "AssassinClass", 
      "BarbarianClass",
        "CartographerClass", 
      "DruidClass",  
      "EnchanterClass", 
      "KnightClass",  
      "MageClass",  
      "RangerClass", 
      "SoldierClass", 
        "TechnicianClass", 
        "BridgeBuilderClass", 
      "WizardClass",  
      ]):
      iTotalValue  = 0;
      aArmy = [];
      curMoney = eEconomy.maxMoney;
      output.log("\nStarting money:" + str(curMoney) + "$");
      output.dump();
      
      
      while (curMoney > 0):
          curChoice = random.choice(aUnitPool);
          
          # If we exceed our money
          if (eEconomy.cost(Game.getInstanceOf(curChoice,  eEconomy,  gameMap)) > curMoney):
              curChoice = None;
              # Try linearly
              for cChoice in aUnitPool:
                # If we have enough money
                if eEconomy.cost(Game.getInstanceOf(cChoice,  eEconomy,  gameMap)) <= curMoney:
                    # buy the army
                    curChoice = cChoice;
              # If we found nothing we can afford
              if (curChoice == None):
                output.log("\nTotal army value: %d$\n"%(iTotalValue));
                # quit
                return aArmy;
          # else buy the army
          armyToAdd = Game.getInstanceOf(curChoice,  eEconomy,  gameMap);
          # assign color
          armyToAdd.color = armyColor;
          
          aArmy.append(armyToAdd);
          output.log("Selected %s for %d$. " %(str(curChoice),  eEconomy.cost(armyToAdd)));
          # update our running total of money
          curMoney -= eEconomy.cost(armyToAdd);
          iTotalValue += eEconomy.cost(armyToAdd);
      output.log("\nTotal army value: %d$\n"%(iTotalValue));
        
  # Class method definitions
  def dealDamage(self, oFrom, oTo):
      output = self.output;
      output.log("%s attacks %s with a %s attack.\t"%(str(oFrom),  str(oTo),  oFrom.damageType) );
      
      actualDefence = oTo.defence;
      
      if oFrom.damageType in oTo.immunities:
        output.log("Target is immune!");
        return oTo;

      if oFrom.damageType in oTo.resistances:
        actualDefence = oTo.defence * 2.0;
      if oFrom.damageType in oTo.vulnerabilities:
        actualDefence = oTo.defence * 0.5;

      dDmg = round(max(oFrom.attack * math.pow(1.05, (10 - actualDefence)), 1.0));
      oTo.currentHp -= dDmg;
      output.log("Target is hit for %d damage. %d hit points remaining."%(dDmg,  oTo.currentHp));

      return oTo;

  def printGameState(self):
      self.output.dump();

  def repaintTerrain(self):
    self.output.drawMap(self.gameMap,  self.aAttackers,  []);

  def interactWithTrap(self,  actor,  trap,  friends,  foes,  traps=[]):
      self.act(actor,  trap,  friends,  foes,  traps);
      if (trap.hp <= 0):
        self.gameMap.traps.remove(trap);
        # Reward actor
        actor.score += self.economy.trapValue(trap);
      else:
        self.act(trap,  actor,  [],  [actor]);
      

      return actor.currentHp > 0;

  def interactWithTreasure(self,  actor,  treasure,  friends,  foes):
      treasure.applyEffectTo(actor);
      self.gameMap.treasures.remove(treasure);
      # Reward actor
      actor.score += self.economy.treasureValue(treasure);
      
      return True;
      
  def interactWithFoe(self,  actor, foe,  friends,  foes):
      self.act(actor,  foe,  friends,  foes);
      self.act(foe,  actor,  foes,  friends);

      if foe.hp < 0:
        # Enemy died
        foes.remove(foe);
        # Reward actor
        actor.score += self.economy.cost(foe);

      return actor.currentHp > 0;
      
  def act(self, actor, target,  friends, foes,  traps = []):
      output = self.output;
      
      if (actor is SoldierClass):
        output.color(actor.color);
      
      # Use abilities, if they exist
      if len(actor.abilities) > 0:
        # DEBUG LINES
        #output.log("Using ability!");
        for aCurAbility in actor.abilities:          
          # DEBUG LINES
          #output.log("Ability group:" + aCurAbility.group);
          
          foe = None;
          if aCurAbility.group == "traps":
            if target in traps:
              foe = target;
            # DEBUG LINES
#            print "Found TRAP!";
#            raw_input();
          else:
            if aCurAbility.group == "foes":
              if target in foes:
                  foe = target;
                  
          # If not applicable as a foe or trap    
          if (foe == None):
            continue;
            
          # Check probability for probability-based abilities
          try:
             if (float(aCurAbility.frequency) > 0) and (float(aCurAbility.frequency) < 1):                  
                fCurProbability = float(aCurAbility.frequency);
                fRoll = random.random();
                if  fRoll <= fCurProbability:
                    # DEBUG LINES
                    #output.log("Rolled %4.2f with a chance of %4.2f"%(fRoll,  fCurProbability));
                    
                    if (aCurAbility.applyTo(foe, friends, foes) != None):
                        output.log(str(aCurAbility));
                continue;
          except:
            # DEBUG LINES
            #output.log("\n" + str(aCurAbility) + "\n");
            pass; # Ignore

          # Try to apply ability for other types of frequency
          if (aCurAbility.applyTo(foe, friends, foes,  traps) != None):
            output.log(str(aCurAbility));
#          else:
#              # DEBUG LINES
#              print "Could not use " + str(type(aCurAbility));
          
          # Remove battle abilities
          if aCurAbility.frequency == "battle": 
              actor.abilities.remove(aCurAbility);
          # Decrease (and possibly remove) abilities with uses
          try:
              if (int(aCurAbility.frequency) >= 1):
                iCurUses = int(aCurAbility.frequency);
                iCurUses -= 1;
                if iCurUses == 0:
                    actor.abilities.remove(aCurAbility);
                else:
                    aCurAbility.frequency = str(iCurUses);
          except:
            pass; # Ignore

      # Deal damage, if target is still a foe
      if target in foes:
        target.currentHp = self.dealDamage(actor, target).currentHp;
      # Reset color 
      output.color();
    
  def __init__(self,  economy,  gameMap,  army,  output,  msgBaseDelaySecs = 0.10):
    # Init map
    self.economy = economy;
    self.gameMap = gameMap;
    self.aAttackers = army;
    # Init output
    self.output = output;
    self.msgBaseDelaySecs = msgBaseDelaySecs;
    
  def run(self):
    output = self.output;
    msgBaseDelaySecs = self.msgBaseDelaySecs;
    
    output.log("Game begins!");
        
    self.dead = [];
    output.dump();
    time.sleep(2 * msgBaseDelaySecs);
    
    # Position armies
    iX = 0; iY = 2;
    for oItemA in self.aAttackers:
        oItemA.x = iX;
        oItemA.y = iY;
        iX += 1;
        if (iX == self.gameMap.xSize):
            iX = 0;
            iY += 1;
            
    # Main game loop
    iGameTime = 0;
    self.repaintTerrain();
    iRowCnt = 0;
    
    while (True):        
        bShouldRepaint = False;
        
        iGameTime += 1; # Next moment
        if (iGameTime % 100 == 0):
          output.log("The time is now %d..."%(iGameTime));
        self.gameTime = iGameTime;        
        bEndConditions = False;
        
        # Local vars
        aAttackers = self.aAttackers;
        
        bActed = False;
        
        for cCurAttacker in aAttackers:
            if (iGameTime % round(1000.0 / cCurAttacker.attackSpeed)) == 0:
              cCurAttacker.act(aAttackers,  self.gameMap.foes,  self);
              # Reduce fullness
              cCurAttacker.fullness -= 1;
              # DEBUG LINES
#              output.log("\n" + str(cCurAttacker) + "\n");
#              output.log(pformat(vars(cCurAttacker)) + "\n");
              bActed = True;
        
            if (cCurAttacker.currentHp <= 0 or cCurAttacker.fullness <= 0):
                output.log(colored("\nAttacker", aAttackers[0].color) + " has died!");
                # Put to dead
                self.dead += [aAttackers[0]];
                self.aAttackers = aAttackers[1:];
                bActed = True;
        
        if (bActed):
            self.repaintTerrain();
            output.log("\n");
            self.printGameState();
            time.sleep(3 * msgBaseDelaySecs);
            iRowCnt += 1;
            if (iRowCnt >= 5 or bShouldRepaint):
                if (bShouldRepaint):
                    time.sleep(10 * msgBaseDelaySecs);
                    iRowCnt = 0;
                
        # TODO: Remove
        bEndConditions = (len(self.aAttackers) == 0) or (iGameTime > 1000);
        # End of game
        if (bEndConditions):
            break;

    dScore = self.getScore(iGameTime,  self.aAttackers);
    output.log("Score: %d after %d time"%(dScore,  iGameTime));
    
    if (len(self.aAttackers) == 0):
        output.log("\n\nNo Attackers left! Defenders win!");
    else:
      output.log("Foraging complete! %d died and %d remain."%(len(self.dead),  len(self.aAttackers)));
    
    

    # Final output
    output.dump();
    return dScore;

  def getScore(self,  iGameTime,  aSurvivors):
    dScore = iGameTime;
    for curSurvivor in aSurvivors:
      dScore += self.economy.cost(curSurvivor) + curSurvivor.score;
    return dScore;

if __name__ == "__main__":
  # Init economy and map
  economy = Economy(5000);
  gameMap = gamemap.GameMap(economy, 20, 20);  
  # Init messaging
  output = ConsoleOutput();
  # Init  army
  # Set colors
  sAttackerColor = "white";
  army = Game.selectArmy(economy,  gameMap,  sAttackerColor,  output);
  # Init game
  g = Game(economy,  gameMap,  army,  output);
    
  
  g.run();
