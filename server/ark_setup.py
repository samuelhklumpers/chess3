from structures.ark.struct import *
from server_rules import *

from structures.structures import *
from utility.util import *
from definitions import *

def setup_ark():
  # player hands
  hands = {}
  for player in ArkPlayer:
    hand = ArkHand([])
    hands[player] = hand

  # drawing stack
  default_stack = jload(os.path.join(DATA_DIR, "default_stack.json"))
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

  # base_move = [[IdMoveRule], [MoveTurnRule], [MovePlayerRule], [FriendlyFireRule]]
  # lazy_drawing = [DrawPieceCMAPRule(), RedrawRule2(), MarkCMAPRule(), MarkRule2()]
  # normal_drawing = lazy_drawing + [DrawSetPieceRule(), SelectRule()]
  # late = [NextTurnRule(), WinCloseRule()


  # setup the rules
  ruleset = game.ruleset = Ruleset()
  ruleset.add_rule(WinStopRule(), -1)

  
  special = [CreatePieceRule({"K": MovedPiece, "p": Pawn, "T": MovedPiece})]

  piece_move = [[PawnSingleRule, PawnDoubleRule, PawnTakeRule, PawnEnPassantRule, KnightRule,
                BishopRule, RookRule, QueenRule, KingRule, CastleRule]]

  move_start, moves, move_end = chain_rules(base_move + piece_move, "move")
  moves.append(SuccesfulMoveRule(move_end))

  post_move = [MovedRule(), PawnPostDouble(), PromoteStartRule(["p"], ["L", "P", "T", "D"]),
                PromoteReadRule(["L", "P", "T", "D"]), WinRule()]

  actions = server_actions()
  actions.append(TouchMoveRule(move_start))

  ruleset.add_rule(ConnectSetupRule({"board_size": (8, 8)}), 0)

  draw_table = {"K": "king.svg", "D": "queen.svg", "T": "rook.svg", "L": "bishop.svg", "P": "knight.svg",
                "p": "pawn.svg"}

  start = "wa8Th8Tb8Pg8Pc8Lf8Ld8De8Ka7pb7pc7pd7pe7pf7pg7ph7p;" \
          "ba1Th1Tb1Pg1Pc1Lf1Ld1De1Ka2pb2pc2pd2pe2pf2pg2ph2p"
  drawing = normal_drawing
  drawing.append(make_markvalid(game, piece_move, move_start))

  drawing.append(DrawReplaceRule(draw_table))

  ruleset.add_all(special + moves + post_move + actions + drawing)
  ruleset.add_all(late, prio=-2)

  game.load_board_str(start)
  ruleset.process("init", ())

  return game