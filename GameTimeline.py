from __future__ import print_function
import json

class GameTimeline(object):
    
    def __init__(self,  filepath="GameTimeline.json"):
        self.filepath = filepath
        self.events = []

    def appendStateActionPair(self, state, action):
      self.events.append({"state": state, "action": action})

    def export(self):
      serializedEvents = json.dumps(self.events, sort_keys=True)
      self.events[:] = []

      print(serializedEvents)

      with open(self.filepath, 'w') as f:
        print(serializedEvents, file=f)


# #######################################
# # Example Usage
# #######################################

# #######################################
# # Initialization.
# #######################################

# gameTimeline = GameTimeline()

# #######################################
# # Append state - action pairs for the whole simulation.
# #######################################

# state = {
#   "treasures": [{"id": "SomeEntity", "pos": {"x": 2, "y": 4}}, {"id": "SomeEntity", "pos": {"x": 4, "y": 4}}],
#   "traps": [{"id": "SomeEntity", "pos": {"x": 1, "y": 5}}, {"id": "SomeEntity", "pos": {"x": 2, "y": 5}}],
#   "allies": [{"id": "SomeEntity", "pos": {"x": 3, "y": 4}}, {"id": "SomeEntity", "pos": {"x": 5, "y": 7}}],
#   "enemies": [{"id": "SomeEntity", "pos": {"x": 1, "y": 6}}, {"id": "SomeEntity", "pos": {"x": 3, "y": 6}}]
# }

# gameTimeline.appendStateActionPair(state, {"text": "something happened", "pos": {"x": 2, "y": 4}})

# state["treasures"][0]["pos"]["x"] = 1

# gameTimeline.appendStateActionPair(state, {"text": "something happened", "pos": {"x": 1, "y": 4}})

# #######################################
# # Export everything at the end of the simulation.
# # The timeline is cleaned after export.
# #######################################

# gameTimeline.export()
