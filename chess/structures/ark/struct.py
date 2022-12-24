"""Basic datastructures for Arkbruh"""

import random
from enum import Enum
from typing import List, Dict

from chess.structures.ark.cards import Card


class ArkTerrain(Enum):
    VOID = 0
    NORMAL = 1
    HIGH = 2
    NOBUILD = 3

    HOME = 4
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
        self.cards = []

    def __iter__(self):
        yield from self.cards


class ArkTurn(Enum):
    ENERGY = -2
    DEPLOY = -1
    ACT = 0
    MOVE = 1
    SKILL = 2
    COMBAT = 3


class ArkPlayer(Enum):
    DEFENDER = 0
    ATTACKER = 1


class ArkPhase(Enum):
    BUILD = -1
    EARLY = 0
    MID = 1
    LATE = 2
    END = 3  # end as in someone won


class ArkHand:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def add(self, card):
        self.cards.append(card)

    def __getitem__(self, key):
        return self.cards[key]

    def __delitem__(self, key):
        del self.cards[key]

    def __iter__(self):
        yield from self.cards

    def __repr__(self) -> str:
        return f"Hand{self.cards}"


class ArkStack:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __iter__(self):
        yield from self.cards

    def draw(self):
        if self.cards:
            card = random.choice(self.cards)
            self.cards.remove(card)
            return card


class ArkBoard:
    def __init__(self, tiles: List[List[ArkTile]]):
        self.tiles = tiles

    def get_tile(self, coord):
        try:
            return self.tiles[coord[0]][coord[1]]
        except:
            return None

    def __iter__(self):
        yield from self.tiles


class ArkField:
    def __init__(self, hands: Dict[ArkPlayer, ArkHand], dp: Dict[ArkPlayer, int], stack: ArkStack, board: ArkBoard):
        self.hands = hands
        self.dp = dp
        self.stack = stack
        self.board = board


class ArkState:
    def __init__(self, field: ArkField):
        self.ruleset = None

        self.phase = ArkPhase.EARLY
        self.turn_num = 0
        self.turn = ArkPlayer.DEFENDER
        self.sub_turn = ArkTurn.ACT

        self.acts_remaining = 2
        self.energy_valid = False

        self.field = field

        self.flag = None
        self.counter = 0

    def has_valid(self, player: ArkPlayer, movetype: ArkTurn):
        #print("has_valid", player, movetype)

        if movetype == ArkTurn.ACT:
            return True  # probably

        # TODO check if e.g. there is a movable piece on the board

        return False
