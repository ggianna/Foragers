from termcolor import colored;
from utils import Utils;
import sys;
import copy;
from gamemap import GameMap;

class Output(object):
  def __init__(self):
    self.msg = "";
    self.nextColor = None;
    self.utils = Utils();
  
  def log(self, msg):
    if (self.nextColor == None):
      self.msg += msg;
    else:
      self.msg += colored(msg, self.nextColor);
    
  def dump(self):
    print self.msg;
    self.msg = "";
    
  def write(self):
    print self.utils.padWithSpaces(self.msg, 79)[0:79],;
    
  def writeln(self):
    print self.utils.padWithSpaces(self.msg, 79)[0:79];
    
  def clear(self):
    self.msg = "";

  def color(self, sColor = None):
    self.nextColor = sColor;
    

  def drawMap(self,  mapToDraw,  attackers,  defenders,  attackersColor,  defendersColor):
      # Clear screen
      self.utils.cls();
      
      mapInstance = copy.deepcopy(mapToDraw);
      
      # Render
      for cItem in  attackers:
          mapInstance.squares[cItem.y][cItem.x] = colored(str(cItem),  attackersColor);
      for cItem in  defenders:
          mapInstance.squares[cItem.y][cItem.x] = colored(str(cItem),  defendersColor);
      # Show
      for curRow in range(mapInstance.ySize):
          for curCol in range(mapInstance.xSize):
              sys.stdout.write(mapInstance.squares[curRow][curCol]);
          sys.stdout.write("\n");
      
      del mapInstance;

if __name__ == "__main__":
    o = Output();
    m = GameMap(10,  10);
    import soldiers;
    s = soldiers.SoldierClass();
    s.x = 3; s.y = 0;
    s2 = soldiers.SoldierClass();
    s2.x = 3; s2.y = 1;
    o.drawMap(m,  [s],  [s2],  "green", "red");
    
