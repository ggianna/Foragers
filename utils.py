import os;

class Utils(object):
  @staticmethod
  def sign(x):
    if (x > 0):
      return 1;
    if (x < 0):
      return -1;
    return 0;

  @staticmethod
  def repeatToLength(stringToExpand, length):
    return (stringToExpand * ((length/len(stringToExpand))+1))[:length];

  @staticmethod
  def padWithSpaces(string, length):
    return string + (" " * (length - len(string)));

  @staticmethod
  def cls():
    os.system(['clear','cls'][os.name == 'nt'])
    

class Point(object):
  def __init__(self):
    self.x = None;
    self.y = None;
  
  def tuple(self):
    return (self.x,  self.y);
    
  def __str__(self):
      return str(self.tuple());
