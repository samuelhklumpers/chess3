from abc import ABC

from utility.util import *
from definitions import *

import os

class Card(ABC):
  def __init__(self, name, cost=-1):
    self.owner = None
    self.name  = name
    self.cost  = cost

class Spell(Card):
  def __init__(self, name, cost=-1):
    super().__init__(name, cost=cost)

class Unit(Card):
  def __init__(self, name, cost=-1):
    super().__init__(name, cost=cost)

    self.promotion_cost   = -1
    self.maxhp            = -1
    self.attack           = -1
    self.defence          = -1
    self.resist           = -1
    self.promoted_maxhp   = -1
    self.promoted_attack  = -1
    self.promoted_defence = -1
    self.promoted_resist  = -1
    self.damage_type      = ""
    self.position         = ""
    self.attack_type      = ""
    self.speed            = -1

    self.hp     = 0
    self.energy = 0
    self.effect = 0
    self.stun   = 0

  def __repr__(self) -> str:
    rep = f"{self.name}(hp={self.hp}, energy={self.energy}, effect={self.effect}, stun={self.stun})"

    return rep

class CardFactory:
  def __init__(self, fn):
    self.fn = fn

  @staticmethod
  def make(identifier):
    cards_json = jload(os.path.join(ARK_DATA_DIR, "cards.json"))
    card = cards_json[identifier]

    if card["type"] == "unit":
      unit = Unit(identifier, cost=card["cost"])

      for (key, value) in card.items():
        setattr(unit, key, value)
    else:
      unit = Spell(identifier, cost=card["cost"])
    
    return unit