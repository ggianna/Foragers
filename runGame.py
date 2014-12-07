#!/usr/bin/python
from soldiers import *;
from towers import *;
from economy import Economy;
from output import Output;
import time;
import math;
import random;
import gamemap;
from pprint import pformat

#import pygame;
#from pygame.locals import *;

from termcolor import colored;
#from utils import Utils;


# Init messaging
output = Output();

class Game(object):
    
  def getInstanceOf(self,  sClassName):
      return eval("soldiers." + sClassName +"(self.economy, self.gameMap)");
      
  # Method definitions
  def selectArmy(self,  eEconomy):
      iTotalValue  = 0;
      aArmy = [];
      curMoney = eEconomy.maxMoney;
      output.log("\nStarting money:" + str(curMoney) + "$");
      output.dump();
      
      aUnitPool = [
#      "ArchmageClass",  
#      "AssassinClass", 
#      "BarbarianClass",
#      "DruidClass",  
#      "EnchanterClass", 
#      "KnightClass",  
#      "MageClass",  
#      "RangerClass", 
#      "SoldierClass"
        "TechnicianClass"
      ];
      while (curMoney > 0):
          curChoice = random.choice(aUnitPool);
          
          # If we exceed our money
          if (eEconomy.cost(self.getInstanceOf(curChoice)) > curMoney):
              curChoice = None;
              # Try linearly
              for cChoice in aUnitPool:
                # If we have enough money
                if eEconomy.cost(self.getInstanceOf(cChoice)) <= curMoney:
                    # buy the army
                    curChoice = cChoice;
              # If we found nothing we can afford
              if (curChoice == None):
                output.log("\nTotal army value: %d$\n"%(iTotalValue));
                # quit
                return aArmy;
          # else buy the army
          armyToAdd = self.getInstanceOf(curChoice);
          # assign color
          armyToAdd.color = self.attackerColor;
          
          aArmy.append(armyToAdd);
          output.log("Selected %s for %d$. " %(str(curChoice),  eEconomy.cost(armyToAdd)));
          # update our running total of money
          curMoney -= eEconomy.cost(armyToAdd);
          iTotalValue += eEconomy.cost(armyToAdd);
      output.log("\nTotal army value: %d$\n"%(iTotalValue));
        
  def dealDamage(self, oFrom, oTo):
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
      output.log("Target is hit for " + str(dDmg) + " damage.");

      oTo.currentHp -= dDmg;
      output.log("Target has now " + str(oTo.currentHp)+ " hit points left...");
      
      return oTo;

  def printGameState(self):
      output.dump();

  def repaintTerrain(self):
    output.drawMap(self.gameMap,  self.aAttackers,  [], 
      self.attackerColor,  "");

  def interactWithTrap(self,  actor,  trap,  friends,  foes):
      self.act(actor,  trap,  friends,  foes);
      self.act(trap,  actor,  [],  [actor]);
      
      if (trap.hp <= 0):
        self.gameMap.traps.remove(trap);

      return actor.currentHp > 0;

  def interactWithTreasure(self,  actor,  treasure,  friends,  foes):
      treasure.applyEffectTo(actor);
      self.gameMap.treasures.remove(treasure);
      
      return True;
      
  def interactWithFoe(self,  actor, foe,  friends,  foes):
      self.act(actor,  foe,  friends,  foes);
      self.act(foe,  actor,  foes,  friends);
      
      return actor.currentHp > 0;
      
  def act(self, actor, target,  friends, foes):     
      if (actor is SoldierClass):
        output.color(actor.color);
      
      # Use abilities, if they exist
      if len(actor.abilities) > 0:
        # DEBUG LINES
        #output.log("Using ability!");
        for aCurAbility in actor.abilities:          
          # DEBUG LINES
          #output.log("Ability group:" + aCurAbility.group);
          
          if isinstance(target,  TrapClass):
            print "Found TRAP!";
            foe = target;
            raw_input();
          else:
            if aCurAbility.group == "foes":
              if target in foes:
                  foe = target;
              else:
                  continue;
              
            # Check probability for probability-based abilities
            try:
               if (float(aCurAbility.frequency) > 0) and (float(aCurAbility.frequency) < 1):                  
                  fCurProbability = float(aCurAbility.frequency);
                  fRoll = random.random();
                  if  fRoll <= fCurProbability:
                      # DEBUG LINES
                      # output.log("Rolled %4.2f with a chance of %4.2f"%(fRoll,  fCurProbability));
                      
                      if (aCurAbility.applyTo(foe, friends, foes) != None):
                          output.log(str(aCurAbility));
                  continue;
            except:
              # DEBUG LINES
              #output.log("\n" + str(aCurAbility) + "\n");
              pass; # Ignore

            # Try to apply ability for other types of frequency
            if (aCurAbility.applyTo(foe, friends, foes) != None):
              output.log(str(aCurAbility));
            else:
                # DEBUG LINES
                print "Could not use " + str(type(aCurAbility));
            
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
    
  def run(self):
    # Init output
    self.output = output;
    output.log("Game begins!");
    
    # Set colors
    self.attackerColor = "white";
    
    # Init map
    self.economy = Economy(500);
    self.gameMap = gamemap.GameMap(self.economy, 20, 20);
    

    self.aAttackers = self.selectArmy(self.economy);
    output.dump();
    time.sleep(0.5);
    
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
        self.gameTime = iGameTime;        
        bEndConditions = False;
        
        # Local vars
        aAttackers = self.aAttackers;
        
        bActed = False;
        
        for cCurAttacker in aAttackers:
            if (iGameTime % round(1000.0 / cCurAttacker.attackSpeed)) == 0:
              cCurAttacker.act(aAttackers,  [],  self);
              # Reduce fullness
              cCurAttacker.fullness -= 1;
              # DEBUG LINES
              output.log("\n" + str(cCurAttacker) + "\n");
              output.log(pformat(vars(cCurAttacker)) + "\n");
              bActed = True;
        
        if (cCurAttacker.currentHp <= 0 or cCurAttacker.fullness == 0):
            output.log(colored("\nAttacker", self.attackerColor) + " has died!");
            self.aAttackers = aAttackers[1:];
            bActed = True;
        
        if (bActed):
            self.repaintTerrain();
            output.log("\n");
            self.printGameState();
            time.sleep(1);
            iRowCnt += 1;
            if (iRowCnt >= 5 or bShouldRepaint):
                if (bShouldRepaint):
                    time.sleep(1);
                    iRowCnt = 0;
                
        # TODO: Remove
        bEndConditions = (len(self.aAttackers) == 0);
        # End of game
        if (bEndConditions):
            break;

    if (len(self.aAttackers) == 0):
        output.log("\n\nNo Attackers left! Defenders win!");

    # Final output
    output.dump();
    
if __name__ == "__main__":
  g = Game();
  g.run();
