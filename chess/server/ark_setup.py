"""Setup functions for Arkbruh"""

import os

from definitions import ARK_DATA_DIR

from chess.structures.ark.struct import (
    ArkPlayer, ArkStack, ArkHand, ArkTile, ArkTerrain, ArkBoard, ArkField, ArkState)
from chess.structures.ark.cards import CardFactory

from chess.structures.structures import Ruleset
from chess.utility.util import jload

#from chess.server.server_rules import *
from chess.rules.ark.basics import *
from chess.rules.ark.drawing import *


def setup_ark():
    # player hands
    hands = {}
    for player in ArkPlayer:
        hand = ArkHand([])
        hands[player] = hand

    # dp
    dp = {}
    for player in ArkPlayer:
        dp[player] = 8

    # drawing stack
    default_stack = jload(os.path.join(ARK_DATA_DIR, "default_stack.json"))
    cards = []
    for (ident, num) in default_stack.items():
        for _ in range(num):
            cards.append(CardFactory.make(ident))

    stack = ArkStack(cards)

    # board
    width = height = 3

    tiles = []
    for _ in range(width):
        tiles_ = []

        for _ in range(height):
            tiles_.append(ArkTile(ArkTerrain.NORMAL))

        tiles.append(tiles_)

    board = ArkBoard(tiles)

    # field
    field = ArkField(hands, dp, stack, board)

    # setup game
    game = ArkState(field)

    # setup the rules
    ruleset = game.ruleset = Ruleset(game)

    web = []
    rules = [WinCheck(), TurnNext(), SubturnNext(), DoCombat(), CountAction(), ActDrawCard(), DrawCard(), InitSubturn(), CanMoveCheck(), SkipSubturn(),
             PlayUnit(), TransactPlayUnit(), PlayUnitFromHand()]
    drawing = [Refresh(), UpdateAct(), UpdateHand(), UpdateTurn()]

    ruleset.add_all(web)
    ruleset.add_all(rules)
    ruleset.add_all(drawing)

    ruleset.process("init", ())

    return game
