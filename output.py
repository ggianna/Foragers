from termcolor import colored;
from utils import Utils;
import sys;
import copy;
from gamemap import GameMap;
from GameTimeline import GameTimeline

class Output(object):
  def log(self, msg): pass;
  def logAction(self, msg, x, y): pass;
  def dump(self): pass
  def write(self): pass
  def writeln(self): pass
  def clear(self): pass
  def color(self,  sColor = None): pass
  def drawMap(self,  mapToDraw,  attackers,  defenders,  trapColor = "red", 
    treasureColor = "yellow", terrainColor = "green"): pass
  def saveToFile(self, sFilename):
    pass

    
class ConsoleOutput(Output):
  def __init__(self):
    self.lastMessages = [];
    self.msg = "";
    self.nextColor = None;
    self.maxMessages = 10;

    self.actions = [];
    self.timeline = GameTimeline();

  def log(self, msg):
    msg = msg.strip();
    
    if (len(msg) == 0):
      return;
      
    if (self.nextColor == None):
      self.msg += "\n" + msg;
      self.lastMessages += [msg];
    else:
      self.msg += colored(msg, self.nextColor);
      self.lastMessages += [colored(msg, self.nextColor)];
    
    if (len(self.lastMessages) > self.maxMessages):
      self.lastMessages = self.lastMessages[-self.maxMessages:];
    
  def logAction(self, msg, x, y):
    self.actions.append({"text": msg, "pos": {"x": x, "y": y}})

  def dump(self):
    # DEBUG LINES
#    print "Messages %d"%(len(self.lastMessages));
    # Keep 5 last messages
    if (len(self.lastMessages) > self.maxMessages):
      self.lastMessages = self.lastMessages[-self.maxMessages:];
      
    print "\n".join(self.lastMessages);
    #self.msg = "";
    
  def write(self):
    print Utils.padWithSpaces(self.msg, 79)[0:79],;
    
  def writeln(self):
    print Utils.padWithSpaces(self.msg, 79)[0:79];
    
  def clear(self):
    #self.msg = "";
    self.lastMessages = [];
    
  def color(self, sColor = None):
    self.nextColor = sColor;

  def drawMap(self,  mapToDraw,  attackers,  defenders,  trapColor = "red", treasureColor = "yellow", terrainColor = "green"):
      # Clear screen
      Utils.cls();

      viewState = {
        "treasures": [],
        "traps": [],
        "allies": [],
        "enemies": []
      }

      mapInstance = copy.deepcopy(mapToDraw);
      # Init squares
      mapInstance.squares = [[ colored('...', terrainColor) for iCnt in range(0, mapInstance.xSize) ] for iCnt in range(0, mapInstance.ySize)];
      
      # Add traps
      for iCnt in range(0,  mapInstance.xSize): 
        for iCnt2 in range(0,  mapInstance.ySize):
          squareTreasures = mapInstance.getTreasures(iCnt, iCnt2);
          squareTraps = mapInstance.getTraps(iCnt, iCnt2);
          squareFoes = mapInstance.getFoes(iCnt, iCnt2);
      
          # If treasure in square
          if (len(squareTreasures)) > 0:
            # Show the first
            mapInstance.squares[iCnt][iCnt2] = colored(str(squareTreasures[0]), treasureColor);

            viewState["treasures"].append({"id": type(squareTreasures[0]).__name__, "pos": {"x": iCnt, "y": iCnt2}})
          else:
            if len(squareFoes) > 0:
              # Show the first
              mapInstance.squares[iCnt][iCnt2] = colored(str(squareFoes[0]), trapColor);

              viewState["traps"].append({"id": type(squareFoes[0]).__name__, "pos": {"x": iCnt, "y": iCnt2}})
            else:
              # If trap in square
              if (len(squareTraps)) > 0:
                # Show the first
                mapInstance.squares[iCnt][iCnt2] = colored(str(squareTraps[0]), trapColor);

                viewState["traps"].append({"id": type(squareTraps[0]).__name__, "pos": {"x": iCnt, "y": iCnt2}})

      # Render soldiers
      for cItem in  attackers:
          mapInstance.squares[cItem.x][cItem.y] = colored(str(cItem),  cItem.color);
          viewState["allies"].append({"id": type(cItem).__name__, "pos": {"x": cItem.x, "y": cItem.y}})
          
      for cItem in  defenders:
          mapInstance.squares[cItem.x][cItem.y] = colored(str(cItem),  cItem.color);
          viewState["enemies"].append({"id": type(cItem).__name__, "pos": {"x": cItem.x, "y": cItem.y}})
                
      # Show map
      for curRow in range(mapInstance.ySize):
          for curCol in range(mapInstance.xSize):
              sys.stdout.write(mapInstance.squares[curCol][curRow]);
          sys.stdout.write("\n");

      # Get rid of deep map copy
      del mapInstance;

      # Append state - action pair for the View engine
      for action in self.actions:
        self.timeline.appendStateActionPair(viewState, action)
      # self.timeline.appendStateActionPair(viewState, {"text": "Something happened", "pos": {"x": 4, "y": 5}})

      self.actions[:] = []


  def saveToFile(self, sFilename):
    fOut = open(sFilename, 'w')
    fOut.write(self.msg)
    fOut.close()

    self.timeline.export()

if __name__ == "__main__":
    o = Output();
    m = GameMap(10,  10);
    import soldiers;
    s = soldiers.SoldierClass();
    s.x = 3; s.y = 0;
    s2 = soldiers.SoldierClass();
    s2.x = 3; s2.y = 1;
    o.drawMap(m,  [s],  [s2],  "green", "red");
    
