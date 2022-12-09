import random

# When the lid is open, it exposes two buttons, top and bottom.
# When the lid is closed, it exposes two lights, top and bottom.
# Only one light is ever glowing at a time. You have to press
# the corresponding button to get a treat. If you press the wrong
# button, then you cannot get the treat by pressing the other button.

class SkinnerBox:
  def __init__(self):
    self._is_lid_open = True
    self._internal_switch = random.randint(0, 1)
    self._is_treat_forbidden = False
    self._is_treat_gotten = False
    self.ALL_ACTIONS = [
      "OPEN_LID",
      "CLOSE_LID",
      "PRESS_BUTTON_TOP",
      "PRESS_BUTTON_BOTTOM"
    ]
    
  def observe(self):
    retval = []
    if self._is_lid_open:
      retval += ["LID_OPEN"]
    else:
      retval += ["LID_CLOSED"]
      if self._internal_switch == 0:
        retval += ["LIGHT_TOP"]
      else:
        retval += ["LIGHT_BOTTOM"]
    if self._is_treat_gotten:
      retval += ["TREAT"]
    return retval
      
  def act(self, action):
    if action == "OPEN_LID":
      self._is_lid_open = True
      return
    if action == "CLOSE_LID":
      self._is_lid_open = False
      return
    if self._is_lid_open:
      if not self._is_treat_forbidden:
        if action == "PRESS_BUTTON_TOP":
          if self._internal_switch == 0:
            self._is_treat_gotten = True
            return
          else:
            self._is_treat_forbidden = True
            return
        elif action == "PRESS_BUTTON_BOTTOM":
          if self._internal_switch == 1:
            self._is_treat_gotten = True
            return
          else:
            self._is_treat_forbidden = True
            return
    
      
    
        
      