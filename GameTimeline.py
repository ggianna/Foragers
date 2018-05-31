from __future__ import print_function
import json

class GameTimeline(object):
    
    def __init__(self,  filepath="GameTimeline.json"):
        self.filepath = filepath;
        self.events = [];

    def appendStateActionPair(self, state, action):
      self.events.append({"state": state, "action": action})

    def export(self):
      serializedEvents = json.dumps(self.events, sort_keys=True)
      self.events[:] = []

      print(serializedEvents)

      with open(self.filepath, 'w') as f:
        print(serializedEvents, file=f)

'''
#######################################
# Example Usage
#######################################

#######################################
# Initialization.
#######################################

gameTimeline = GameTimeline()

#######################################
# Append state - action pairs for the whole simulation.
#######################################

gameTimeline.appendStateActionPair({"hi": "mate"}, {"text": "Did stuff", "x": 2, "y": 4})
gameTimeline.appendStateActionPair({"hey": "dude"}, {"text": "Did stuff 2", "x": 3, "y": 6})

#######################################
# Export everything at the end of the simulation.
# The timeline is cleaned after export.
#######################################

gameTimeline.export()
'''