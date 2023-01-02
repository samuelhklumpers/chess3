"""Setup functions for Arkbruh"""

import os

from definitions import ARK_DATA_DIR

from chess.structures.ark.struct import (
    ArkPlayer, ArkStack, ArkHand, ArkTile, ArkTerrain, ArkBoard, ArkField, ArkState)
from chess.structures.ark.cards import CardFactory

from chess.structures.structures import Ruleset
from chess.utility.util import jload

from chess.rules.ark.basics import *
from chess.rules.ark.drawing import *
from chess.rules.ark.turns import *
from chess.rules.ark.actions import *
from chess.rules.ark.ui import *
from chess.rules.ark.movement import *


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
    for x in range(width):
        tiles_ = []

        for y in range(height):
            tiles_.append(ArkTile(ArkTerrain.NORMAL, x, y))

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
             PlaceUnit(), TransactPlayCard(), PlaceUnitFromHand()]
    ui = [UserClickUnit(), UserClickTile()]
    movement = [InitMove(), MoveUnit()]
    turn = [PassiveDPGain(), InitAction(), CountSubaction()]
    action = [PromoteUnit(), PromoteCardRule()]
    drawing = [Refresh(), UpdateAct(), UpdateHand(), UpdateTurn(),
               UpdateDP(), UpdateTile(), UpdateSubact()]
    init = [Init()]

    ruleset.add_all(web)
    ruleset.add_all(rules)
    ruleset.add_all(ui)
    ruleset.add_all(movement)
    ruleset.add_all(turn)
    ruleset.add_all(drawing)
    ruleset.add_all(action)
    ruleset.add_all(init)

    ruleset.process("init", ())

    return game
