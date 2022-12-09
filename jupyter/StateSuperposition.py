from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

import random
import copy

# A superposition of states can still be acted on and observed,
# but it returns sets of possibilities from all of the states
# from which it's comprised.

# Later this will be adapted to handle probabilities.

class StateSuperposition:
  def __init__(self):
    self.states = []


  def __repr__(self) -> str:
    s = f"Super:{len(self.states)}"
    return s
    
    
  def add_state(self, state):
    for oldstate in self.states:
      if oldstate == state:
        # State is already in our state set! Maybe adjust its probability if we're doing that.
        return
    self.states.append(state)


  # Returns the union of all actions takeable in all comprising states.
  def generate_possible_actions(self) -> set:
    retval = set()
    for state in self.states:
      retval = retval.union(state.generate_possible_actions())
    return retval


  # Returns observations that we might make in this superposition, and
  # the states that might produce said observations.
  def observe(self) -> set:    
    # We want to use a list of tuples rather than a set or dict, because
    # the observation object might not be mutable.
    retval = []
    
    for state in self.states:
      obs = state.observe()
      
      # Check if a compatible observation already exists in the retval collection.
      # NOTE: Our compatibility function might someday be state dependent. Right now
      # it's just a simple equality comparison.
      is_observation_already_expected = False
      for retobs, retsuper in retval:
        if retobs == obs:
          is_observation_already_expected = True
          retsuper.add_state(state)
          
      if not is_observation_already_expected:
        newsuper = StateSuperposition()
        newsuper.add_state(state)
        retval.append( (obs, newsuper) )
      
    return retval
      

  
  # Returns True iff any comprising state's observation contains the requested symbol.
  def could_produce_observation(self, obs: str) -> bool:
    all_obses = observe()
    for obsset in all_obses:
      if obs in obsset:
        return True
    return False
    
  
  
  # Returns a superposition of states that may arise from taking this
  # action in this current superposition.
  # NOTE: May make this an iterator in the future.
  def act(self, action: str) -> StateSuperposition:
    nextsuperstate = StateSuperposition()

    for oldstate in self.states:
      nextstate = oldstate.act(action)
      nextsuperstate.add_state(nextstate)
    
    return nextsuperstate
    
      
    
        
      