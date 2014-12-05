class GameMap(object):
    def __init__(self,  xSize=10,  ySize=10):
        self.xSize = xSize;
        self.ySize = ySize;
        
        # Init squares
        self.squares = [["..." for iCnt in range(0,  xSize) ] for iCnt2 in range(0,  ySize)];
