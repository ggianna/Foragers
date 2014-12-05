#!/usr/bin/python
from soldiers import *;
from towers import *;
from economy import Economy;
from output import Output;
import time;
import math;
import random;
import gamemap;

import sys;
import select;
#import pygame;
#from pygame.locals import *;

from termcolor import colored;
#from utils import Utils;


# Init messaging
output = Output();

class Game(object):
    
  def getInstanceOf(self,  sClassName):
      return eval("soldiers." + sClassName +"()");
      
  # Method definitions
  def selectArmy(self,  eEconomy):
      iTotalValue  = 0;
      aArmy = [];
      curMoney = eEconomy.maxMoney;
      output.log("\nStarting money:" + str(curMoney) + "$");
      output.dump();
      
      aUnitPool = [
      "ArchmageClass",  
      "AssassinClass", 
      "BarbarianClass",
      "DruidClass",  
      "EnchanterClass", 
      "KnightClass",  
      "MageClass",  
      "RangerClass", 
      "SoldierClass"
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
#      output.color(self.attackerColor);
#      output.log("\nAtt:" + " ".join([(str(x)) for x in self.aAttackers])) ;
#      output.color(self.defenderColor);
#      output.log("\tDef:" + " ".join([(str(x)) for x in self.aDefenders]));
#      output.color();
      output.dump();

  def repaintTerrain(self):
    output.drawMap(self.gameMap,  self.aAttackers,  self.aDefenders, 
      self.attackerColor,  self.defenderColor);

    
  def act(self, actor, friends, foes, friendColor, foeColor):
      output.color(friendColor);
      
      # Use abilities, if they exist
      if (len(actor.abilities) > 0):
        # DEBUG LINES
        #output.log("Using ability!");
        for aCurAbility in actor.abilities:
          
          # DEBUG LINES
          #output.log("Ability group:" + aCurAbility.group);
          if aCurAbility.group == "foes":
            if (len(foes) > 0):
                foe = foes[0];
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


	    
	    

      # Deal damage, if anyone left
      if (len(foes) > 0):
        foes[0].currentHp = self.dealDamage(actor, foes[0]).currentHp;
      # Reset color
      output.color();
    
  def run(self):
    output.log("Game begins!");
    
    # Init map
    self.gameMap = gamemap.GameMap(10, 10);
    self.eEconomy = Economy(10000);
    
    # Init fighters
    #aDefenders = [TowerClass(), Fort(), FireElementalistTower(), WaterElementalistTower()];
    self.aDefenders = self.selectArmy(self.eEconomy);
    output.dump();
    time.sleep(1);
    self.aAttackers = self.selectArmy(self.eEconomy);
    output.dump();
    time.sleep(1);
    
    # Position armies
    iX = 0; iY = 2;
    for oItemA in self.aAttackers:
        oItemA.x = iX;
        oItemA.y = iY;
        iX += 1;
        if (iX == self.gameMap.xSize):
            iX = 0;
            iY += 1;

    iX = 0; iY = 0;
    for oItemD in self.aDefenders:
        oItemD.x = iX;
        oItemD.y = iY;
        iX += 1;
        if (iX == self.gameMap.xSize):
            iX = 0;
            iY += 1;

    # Set colors
    self.attackerColor = "yellow";
    self.defenderColor = "green";


    # Main game loop
    iGameTime = 0;
    self.repaintTerrain();
    iRowCnt = 0;
    
    while (True):
        bShouldRepaint = False;
        
        iGameTime += 1; # Next moment
        bEndConditions = False;
        
        # Local vars
        aAttackers = self.aAttackers;
        aDefenders = self.aDefenders;
        
        cCurAttacker = aAttackers[0];
        cCurDefender = aDefenders[0];
        
        bActed = False;
        if (iGameTime % round(1000.0 / cCurAttacker.attackSpeed)) == 0:
          self.act(cCurAttacker, aAttackers, aDefenders, self.attackerColor, self.defenderColor);
          bActed = True;

        if (iGameTime % round(1000.0 /cCurDefender.attackSpeed)) == 0:
          self.act(cCurDefender, aDefenders, aAttackers, self.defenderColor, self.attackerColor);
          bActed = True;

        if (cCurAttacker.currentHp <= 0):
            output.log(colored("Attacker", self.attackerColor) + " has died!");
            self.aAttackers = aAttackers[1:];
            bActed = True;
        if (cCurDefender.currentHp <= 0):
            output.log(colored("Defender", self.defenderColor) + " has died!");
            bShouldRepaint = True;
            self.aDefenders = aDefenders[1:];
            bActed = True;
        
        if (bActed):
            self.repaintTerrain();
            output.log("\n");
            self.printGameState();
            time.sleep(2);
            iRowCnt += 1;
            if (iRowCnt >= 5 or bShouldRepaint):
                if (bShouldRepaint):
                    time.sleep(2);
                    iRowCnt = 0;
                
        # TODO: Remove
        bEndConditions = (len(self.aAttackers) == 0) or (len(self.aDefenders) == 0);
        # End of game
        if (bEndConditions):
            break;

    if (len(self.aAttackers) == 0):
        output.log("\n\nNo Attackers left! Defenders win!");
    if (len(self.aDefenders) == 0):
        output.log("\n\nNo Defenders left! Attackers win!");

    # Final output
    output.dump();
    
if __name__ == "__main__":
  g = Game();
  g.run();
