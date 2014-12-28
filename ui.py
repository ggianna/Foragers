#!/usr/bin/python
class UI(object):
  def getInput(self, inputQuestion):
    pass
  
  def __printMenu(self,dOptionToFunction):
    dKeyToOption = dict()
    iCnt = 0
    for sCurOption in dOptionToFunction.keys():
      dKeyToOption[str(iCnt)] = sCurOption
      print "%d for %s"%(iCnt, sCurOption)
      iCnt+=1
    return dKeyToOption
      
  def menu(self, dOptionToFunction):
    dKeyToOption = self.__printMenu(dOptionToFunction)
    
    sResp = raw_input()
    while not (sResp in dKeyToOption.keys()):
      print "\nWARNING: INVALID OPTION\nPlease select a valid option (From zero to %d)."%(len(dKeyToOption) - 1)
      dKeyToOption = self.__printMenu(dOptionToFunction)
      sResp = raw_input()

    dOptionToFunction[dKeyToOption[sResp]]()
    
  
if __name__ == "__main__":
  import sys
  ui = UI()
  ui.menu({"Test1" : lambda : sys.stdout.write("1 run!\n"),
	   "Test2" : lambda : sys.stdout.write("2 run!\n")})
