from enum import Enum
import random
from typing import *

from cards import *


class ArkTerrain(Enum):
  VOID    = 0
  NORMAL  = 1
  HIGH    = 2
  NOBUILD = 3

  HOME  = 4
  SPAWN = 5

class ArkDamageType(Enum):
  PHYS = 0
  ARTS = 1
  HEAL = 2

class ArkAttackType(Enum):
  AOE = 0
  ST = 1

class ArkTile:
  def __init__(self, terrain=ArkTerrain.VOID):
    self.terrain = terrain
    self.cards   = []

class ArkTurn(Enum):
  ACT    = 0
  MOVE   = 1
  SKILL  = 2
  COMBAT = 3

class ArkPlayer(Enum):
  DEFENDER = 0
  ATTACKER = 1

class ArkPhase(Enum):
  BUILD = -1
  EARLY = 0
  MID   = 1
  LATE  = 2
  END   = 3 # end as in someone won

class ArkHand:
  def __init__(self, cards: List[Card]):
    self.cards = cards

  def add(self, card):
    self.cards.append(card)

class ArkStack:
  def __init__(self, cards: List[Card]):
    self.cards = cards

  def draw(self):
    if self.cards:
      card = random.choice(self.cards)
      self.cards.remove(card)
      return card

class ArkBoard:
  def __init__(self, tiles: List[List[ArkTile]]):
    self.tiles = tiles

class ArkField:
  def __init__(self, hands: Dict[ArkPlayer, ArkHand], stack: ArkStack, board: ArkBoard):
    self.hands = hands
    self.stack = stack
    self.board = board

class ArkState:
  def __init__(self, field: ArkField):
    self.ruleset  = None

    self.phase    = ArkPhase.EARLY
    self.turn_num = 0
    self.turn     = ArkPlayer.DEFENDER
    self.sub_turn = ArkTurn.ACT

    self.acts_remaining = 2
    self.energy_valid   = False

    self.field = field