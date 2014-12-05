import os

class Utils(object):
  def repeatToLength(self, stringToExpand, length):
    return (stringToExpand * ((length/len(stringToExpand))+1))[:length];

  def padWithSpaces(self, string, length):
    return string + (" " * (length - len(string)));

  def cls(self):
    os.system(['clear','cls'][os.name == 'nt'])
