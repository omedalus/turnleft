from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

import random
import copy

from Observation import Observation

# When the lid is open, it exposes two buttons, top and bottom.
# When the lid is closed, it exposes two lights, top and bottom.
# Only one light is ever glowing at a time. You have to press
# the corresponding button to get a treat. If you press the wrong
# button, then you cannot get the treat by pressing the other button
# (this prevents a winning strategy of button-mashing).

# Because this is a State, this isn't a "real" box. It's a conceptual
# model of a box. When one submits an action to it, it returns
# a new state that will be created when that action is performed
# in this state.

# Later we will introduce uncertainty. This can take the form of a
# set of emitted states per action. Alternatively, it can take the
# form of a list of observables, and a list of possible values for
# each observable. Basically, either the state itself can be in a
# superposition, or the observables within a state can be in
# superpositions (sub-superpositions, basically?).

# Ideally, a State should also include a hash function
# so that we can mark states as having been visited.

class LampButtonBoxState:
  def __init__(self):
    self._is_lid_open = True
    self._internal_switch = random.randint(0, 1)
    self._is_treat_forbidden = False
    self._is_treat_gotten = False

    # Add tree navigation data to make this state object
    # usable in a planning search.
    self.prev_state = None
    self.action_from_prev_state = None
    self.cost = 0

    
  def __eq__(self, other) -> bool:
    if self._is_lid_open != other._is_lid_open:
      return False 
    if self._internal_switch != other._internal_switch:
      return False 
    if self._is_treat_forbidden != other._is_treat_forbidden:
      return False 
    if self._is_treat_gotten != other._is_treat_gotten:
      return False 
    return True
  
    
  
  def generate_possible_actions(self) -> set:
    # Someday this will be an iterator.
    retval = set([
      "OPEN_LID",
      "CLOSE_LID",
      "PRESS_BUTTON_TOP",
      "PRESS_BUTTON_BOTTOM"
    ])
    return retval
      
    
  def observe(self) -> Observation:
    retval = Observation()
    if self._is_lid_open:
      retval.add("LID_OPEN")
    else:
      retval.add("LID_CLOSED")
      if self._internal_switch == 0:
        retval.add("LIGHT_TOP")
      else:
        retval.add("LIGHT_BOTTOM")
    if self._is_treat_gotten:
      retval.add("TREAT")
    if self._is_treat_forbidden:
      retval.add("ZAP")
    return retval

  
  def act(self, action: str) -> LampButtonBoxState:
    # NOTE: In the future, this might be an iterator.
    # It'll output one possible consequence of this action in this state at a time.
    
    nextstate = copy.deepcopy(self)
    nextstate.prev_state = self
    nextstate.action_from_prev_state = action
    nextstate.cost += 1
    
    if action == "OPEN_LID":
      nextstate._is_lid_open = True
      return nextstate

    if action == "CLOSE_LID":
      nextstate._is_lid_open = False
      return nextstate

    if action == "PRESS_BUTTON_TOP" or action == "PRESS_BUTTON_BOTTOM":
      if not nextstate._is_lid_open:
        # Can't press buttons when the lid is closed!
        # The action itself is invalid and does nothing.
        return nextstate

      is_game_over = nextstate._is_treat_gotten or nextstate._is_treat_forbidden
      if is_game_over:
        return nextstate

      # If the game isn't over and the buttons are pressable,
      # then the button press must actually do something.
      
      if action == "PRESS_BUTTON_TOP":
        if nextstate._internal_switch == 0:
          nextstate._is_treat_gotten = True
        else:
          nextstate._is_treat_forbidden = True
        
      elif action == "PRESS_BUTTON_BOTTOM":
        if nextstate._internal_switch == 1:
          nextstate._is_treat_gotten = True
        else:
          nextstate._is_treat_forbidden = True
          
      return nextstate
    
      
    
        
      