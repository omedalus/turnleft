# A collection of symbols that can be observed while in a state.

# For now, this is implemented as an ordered list of strings.
# Maybe in the future it'll be an iterator or something.

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

import json

class Observation:
  def __init__(self):
    self.symbols = []
    
    
  def add(self, symbol: str) -> None:
    self.symbols.append(symbol)
    self.symbols.sort()
    
  def has(self, symbol: str) -> bool:
    retval = symbol in self.symbols
    return retval


  def toJSON(self) -> str:
    s = json.dumps(self.symbols)
    return s
  
  
  def __eq__(self, other: Observation) -> bool :
    retval = self.toJSON() == other.toJSON()
    return retval
  
  
  def __lt__(self, other: Observation) -> bool :
    retval = self.toJSON() < other.toJSON()
    return retval
  
  
  def __hash__(self) -> int:
    retval = hash(self.toJSON())
    return retval
  
  def __repr__(self) -> str:
    return self.toJSON()
  
  
    
        
      