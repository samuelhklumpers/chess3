from rules.ark.web import ArkWebSocketRule
from structures.ark.struct import *
from server.server_rules import *

from structures.structures import *
from utility.util import *
from definitions import *

from rules.ark.basics import *
from rules.ark.drawing import *


def setup_ark():
  # player hands
  hands = {}
  for player in ArkPlayer:
    hand = ArkHand([])
    hands[player] = hand

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
  field = ArkField(hands, stack, board)

  # setup game
  game = ArkState(field)

  # setup the rules
  ruleset = game.ruleset = Ruleset(game)
  
  web = []
  rules = [WinCheck(), TurnNext(), SubturnNext(), DoCombat(), CountAction(), ActDrawCard(), DrawCard(), InitSubturn(), CanMoveCheck(), SkipSubturn()]
  drawing = [Refresh(), UpdateAct(), UpdateHand(), UpdateTurn()]

  ruleset.add_all(web)
  ruleset.add_all(rules)
  ruleset.add_all(drawing)

  ruleset.process("init", ())

  return game