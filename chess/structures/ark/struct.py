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


class ArkTurn(Enum):
    ACT = 0
    MOVE = 1
    SKILL = 2
    COMBAT = 3


class ArkAction(Enum):
    DRAW = -1
    NONE = 0
    DEPLOY = 1
    ENERGY = 2
    RETREAT = 3


class ArkPlayer(Enum):
    DEFENDER = 0
    ATTACKER = 1


class ArkPhase(Enum):
    BUILD = -1
    EARLY = 0
    MID = 1
    LATE = 2
    END = 3  # end as in someone won


class ArkTile:
    def __init__(self, terrain=ArkTerrain.VOID, x=-1, y=-1):
        self.terrain = terrain
        self.cards = []
        
        self.x = x
        self.y = y

    def __iter__(self):
        yield from self.cards

    def __repr__(self):
        return "Tile[" + "\n".join(repr(c) for c in self) + "]"

        

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

    def get_all_cards(self, player: ArkPlayer = None):
        if player is not None:
            return [card for tile in self for card in tile if card.owner == player]

        return [card for tile in self for card in tile]

    def __iter__(self):
        for row in self.tiles:
            yield from row


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
        self.subturn = ArkTurn.ACT

        self.last_action = ArkAction.NONE
        self.action = ArkAction.NONE
        self.sub_actions_remaining = 0

        self.actions_remaining = 2
        self.energy_valid = False

        self.last_moved_unit = None
        self.selected_unit = None

        self.field = field

    def has_valid(self, player: ArkPlayer, movetype: ArkTurn):
        #print("has_valid", player, movetype)

        if movetype == ArkTurn.ACT:
            return True  # probably

        # check if e.g. there is a movable piece on the board
        if movetype == ArkTurn.MOVE:
            return any([card.movements_remaining > 0 for card in self.field.board.get_all_cards(player=player)])

        return False

    def get_energy_flux(self):
        # return the number of defenders on the board
        return len(self.field.board.get_all_cards(player=ArkPlayer.DEFENDER))