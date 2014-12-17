#!/usr/bin/python
import pygame
from pygame.locals import *
from runGame import Game
from output import Output
from spritesheet import Spritesheet
from economy import Economy
import gamemap
import copy
 
class App(Game,  Output):
    # Output parameter has been removed (because the output is the app object itself
    def __init__(self,  economy,  gameMap,  army,  msgBaseDelaySecs = 0.10):
        # Init GAME parent
        Game.__init__(self,  economy,  gameMap,  army,  output,  msgBaseDelaySecs)
        self._running = True
        self.screen = None
        
        # Init for Output part
        self.lastMessages = [];
        self.msg = "";
        self.nextColor = (128,  128,  128);
        self.msgBaseDelaySecs = msgBaseDelaySecs;
        self.maxMessages = 10;
 
    # Game overrides
    def run(self):
      self.on_execute()
      return self.finalScore
    
    # App methods
    def on_init(self):
        self._running = True
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 20)
        self.TILE_HEIGHT = 32
        self.TILE_WIDTH = 32
        self.MESSAGE_BOX_WIDTH = 400
        self.size = self.weight, self.height = self.gameMap.xSize * self.TILE_WIDTH + self.MESSAGE_BOX_WIDTH, \
          self.gameMap.ySize * self.TILE_HEIGHT
        self.msgBoxLeft = self.gameMap.xSize * self.TILE_WIDTH
        self.output = self
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
#        msgBaseDelaySecs = self.msgBaseDelaySecs;
        
        # Default spritesheet assets
        self.sprites = Spritesheet("assets/fantasy-tileset-8cols-26rows-32x32pixels.png")
        self.enemySprites = Spritesheet("assets/fantasy-tileset-8cols-26rows-32x32pixels-red.png")
        
        output = self.output;
        self.iGameTime = 0;
        
        output.log("Game begins!");
            
        self.dead = [];
        output.dump();
#        time.sleep(2 * msgBaseDelaySecs);
        
        # Position armies
        iX = 0; iY = 2;
        for oItemA in self.aAttackers:
            oItemA.x = iX;
            oItemA.y = iY;
            iX += 1;
            if (iX == self.gameMap.xSize):
                iX = 0;
                iY += 1;

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            
    def on_loop(self):
      # If stopped running
      if not self._running:
        # Quit the loop
        return
        
      # Main game loop
      output = self.output;
      iGameTime = self.iGameTime;
#      msgBaseDelaySecs = self.msgBaseDelaySecs;
      
      iGameTime += 1; # Next moment
      if (iGameTime % 100 == 0):
        output.log("The time is now %d..."%(iGameTime));
      self.iGameTime = iGameTime;        
      bEndConditions = False;
      
      # Local vars
      aAttackers = self.aAttackers;
      
      bActed = False;
      
      for cCurAttacker in aAttackers:
          if (iGameTime % round(1000.0 / cCurAttacker.attackSpeed)) == 0:
            cCurAttacker.act(aAttackers,  self.gameMap.foes,  self);
            # Reduce fullness
            cCurAttacker.fullness -= 1;
            bActed = True;
      
          if (cCurAttacker.currentHp <= 0 or cCurAttacker.fullness <= 0):
              output.log("\nAttacker has died!");
              # Put to dead
              self.dead += [aAttackers[0]];
              self.aAttackers = aAttackers[1:];
              bActed = True;
      
      if (bActed):
          self.repaintTerrain();
          self.printGameState();
      else:
          self.printGameState();
#          time.sleep(3 * msgBaseDelaySecs);

      # End of game
      bEndConditions = (len(self.aAttackers) == 0) or (iGameTime > 1000);
      if (bEndConditions):
          self._running = False;


    def on_render(self):
        self.repaintTerrain()
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            
        dScore = self.getScore(self.iGameTime,  self.aAttackers);
        output.log("Score: %d after %d time"%(dScore,  self.iGameTime));
        
        if (len(self.aAttackers) == 0):
            output.log("\n\nNo Attackers left! Defenders win!");
        else:
          output.log("Foraging complete! %d died and %d remain."%(len(self.dead),  len(self.aAttackers)));
        
        # Final output
        output.dump();
        self.finalScore = dScore
        
        self.on_cleanup()
        
        
    # Output object override
    
    def log(self, msg): 
        msg = msg.strip();
        
        if (len(msg) == 0):
          return;
          
        if (self.nextColor == None):
          self.nextColor = (128, 128, 128)
        else:
          # Round robin in color
          tmpColor = [];
          for iColorCnt in range(3):
            if (self.nextColor[iColorCnt] + 4) > 255:
              tmpColor += [128]
            else:
              tmpColor += [self.nextColor[iColorCnt] + 4]
          self.nextColor = tuple(tmpColor)
            
        self.msg += msg;
        self.lastMessages += [(msg,  self.nextColor)];
        
        if (len(self.lastMessages) > self.maxMessages):
          self.lastMessages = self.lastMessages[-self.maxMessages:];

    def dump(self):
        if (len(self.lastMessages) > self.maxMessages):
          self.lastMessages = self.lastMessages[-self.maxMessages:];
          
          # DEBUG LINES
#        print "\n".join(self.lastMessages);
        
        iMsgY = 0
        for curMsg in self.lastMessages:
          msgImg = self.font.render(curMsg[0], 0, curMsg[1], (0, 0,  0))
          msgRect = msgImg.get_rect()
          msgDstRect = Rect(self.msgBoxLeft, iMsgY  , msgRect.width,  msgRect.height)
          # Update screen
          self.screen.blit(msgImg,   msgDstRect)
          iMsgY += msgRect.height + 5
          
        self.msg = "";
      
    # TODO: Implement (?)
    def write(self): pass
    def writeln(self): pass

    def clear(self): 
        self.msg = "";
        self.lastMessages = [];

      
    def color(self,  sColor = None):
        self.nextColor = sColor;
        
    def drawMap(self,  mapToDraw,  attackers,  defenders,  trapColor = (255, 0, 0), 
      treasureColor = (0, 255, 255), terrainColor = (0,  255,  255)):

      # ZERO-BASED row,col for default spritesheet  (assets/fantasy-tileset-8cols-26rows-32x32pixels.png)
      # Define mapping between ASCII and image representation
      # Soldiers
      SOLDIERS_ROW = 18;
      isSoldier = lambda x: x.lower()[0] in [" ",  "/",  "_"];
      ASSASIN_COL = 0;
      DRUID_COL = 1;
      BARBARIAN_COL = 2;
      SOLDIER_COL = 3;
      RANGER_COL = 4;
      KNIGHT_COL = 5;
      MAGE_COL = 6;
      ENCHANTER_COL = 6; # TODO: Find other icon
      WIZARD_COL = 7;
      
      soldierMap = {"X":  ASSASIN_COL, 
        "D": DRUID_COL, 
        "B": BARBARIAN_COL, 
        "S" : SOLDIER_COL, 
        "R" : RANGER_COL, 
        "K" : KNIGHT_COL, 
        "M" : MAGE_COL, 
        "E" : ENCHANTER_COL, 
        "W" : WIZARD_COL
        }
      
      # Towers
      TOWERS_ROW = 14;
      isTower = lambda x: x.lower()[0] in ["|",  ">",  ","];
      FIRE_ELEMENTALIST_COL = 1;
      FORT_COL = 3
      ILLUSIONIST_COL = 6
      TOWER_COL = 0
      WIZARD_TOWER_COL = 4
      towerMap = {"E" :  FIRE_ELEMENTALIST_COL,  "F" : FORT_COL,  
        "I" : ILLUSIONIST_COL,  "T" :  TOWER_COL,"W" : WIZARD_TOWER_COL,};

      # Traps
      TRAPS_ROW = 2;
      isTrap = lambda x: x.lower()[1] in ["^",  "_",  "@",  "*"];
      ARROWSLIT_COL = 1;
      EXPLOSION_COL = 0
      LABYRINTH_COL = 3
      PIT_COL = 4
      TRAPCLASS_COL = 1
      trapMap = {"^" :  ARROWSLIT_COL,  "*" : EXPLOSION_COL,  
        "@" : LABYRINTH_COL,  "_" :  PIT_COL,"#" : TRAPCLASS_COL,};
      
      # Fields
      FIELD_ROW = 0
      FIELD_COL = 3
      
      # Treasures
      TREASURE_ROW = 15
      TREASURE_COL = 1
      
      mapInstance = copy.deepcopy(mapToDraw);
      # Init squares
      mapInstance.squares = [[ '...' for iCnt in range(0, mapInstance.xSize) ] for iCnt in range(0, mapInstance.ySize)];
      isTerrain = lambda x : x == "..."
      
      # Init map ASCII representation
      for iCnt in range(0,  mapInstance.xSize): 
        for iCnt2 in range(0,  mapInstance.ySize):
          squareTreasures = mapInstance.getTreasures(iCnt, iCnt2);
          squareTraps = mapInstance.getTraps(iCnt, iCnt2);
          squareFoes = mapInstance.getFoes(iCnt, iCnt2);
      
          # If treasure in square
          if (len(squareTreasures)) > 0:
            # Show the first
            mapInstance.squares[iCnt][iCnt2] = str(squareTreasures[0]);
          else:
            if len(squareFoes) > 0:
              # Show the first
              mapInstance.squares[iCnt][iCnt2] = str(squareFoes[0]);
            else:
              # If trap in square
              if (len(squareTraps)) > 0:
                # Show the first
                mapInstance.squares[iCnt][iCnt2] = str(squareTraps[0]);
      
      # Render soldiers
      for cItem in  attackers:
          # Indicate attackers with starting A letter
          mapInstance.squares[cItem.x][cItem.y] = "A" + str(cItem);
      for cItem in  defenders:
          mapInstance.squares[cItem.x][cItem.y] = str(cItem);
                
      
      # Show map
      for curRow in range(mapInstance.ySize):
          for curCol in range(mapInstance.xSize):
              sCurSq = mapInstance.squares[curCol][curRow]
              
              sprites = self.enemySprites
              if sCurSq[0] == "A":
                sprites = self.sprites
                sCurSq = sCurSq[1:]
              else:
                if isTerrain(sCurSq):
                  sprites = self.sprites

                
              img = None
              if isSoldier(sCurSq):
                img = sprites.image_at_col_row(soldierMap[sCurSq[1]],  SOLDIERS_ROW)
              if isTower(sCurSq):
                img = sprites.image_at_col_row(towerMap[sCurSq[1]],  TOWERS_ROW)
              if isTrap(sCurSq):
                img = sprites.image_at_col_row(trapMap[sCurSq[1]],  TRAPS_ROW)
              if isTerrain(sCurSq):
                img = sprites.image_at_col_row(FIELD_COL,  FIELD_ROW)
              if img == None: # Treasure
                img = sprites.image_at_col_row(TREASURE_COL,  TREASURE_ROW)

              TILE_HEIGHT = self.TILE_HEIGHT
              TILE_WIDTH = self.TILE_WIDTH
              src = Rect(0,  0,  TILE_WIDTH,  TILE_HEIGHT)
              dst = Rect(curCol * TILE_WIDTH,  curRow * TILE_HEIGHT,  TILE_WIDTH,  TILE_HEIGHT)
              self.screen.blit(img,  dst,  src)

      # Get rid of deep map copy
      del mapInstance;
      
      # Actually render
      pygame.display.flip()
    
if __name__ == "__main__" :
    # Init economy and map
    economy = Economy(5000);
    gameMap = gamemap.GameMap(economy, 20, 20);  
    output = Output()
    # Init  army
    # Set colors
    sAttackerColor = (255,  255,  255);
    army = Game.selectArmy(economy,  gameMap,  sAttackerColor,  output,  
      [
      "AssassinClass", 
      "BarbarianClass",
      "DruidClass",  
      "EnchanterClass", 
      "KnightClass",  
      "MageClass",  
      "RangerClass", 
      "SoldierClass", 
      "WizardClass",  
#        "CartographerClass", 
#        "TechnicianClass", 
#        "BridgeBuilderClass", 
      ]);
    theApp = App(economy,  gameMap, army)
    theApp.on_execute()
