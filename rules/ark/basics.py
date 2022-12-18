from rules.rules import *
from structures.ark.struct import *
from structures.ark.cards import *

class WinCheck(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["combat_done"])

    def process(self, game: ArkState, effect: str, args):
        # check if someone has won

        return [("win_check_false", [effect])]

class TurnEnd(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["win_check_false"])

    def process(self, game: ArkState, effect: str, args):
        # if combat has ended, and there is no winner yet, signal the end of the current turn
        if args[0] == "combat_done":
            return [("turn_end", [])]

class TurnNext(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["turn_end"])

    def process(self, game: ArkState, effect: str, args):
        # if the current turn has ended, but the game is not over yet, signal the start of the next turn
        if game.phase != ArkPhase.END:
            return [("turn_next", [])]

class CountAction(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["act_draw_card"])

    def process(self, game: ArkState, effect: str, args):
        if game.acts_remaining > 0:
            game.acts_remaining -= 1
        else:
            return [("player_act_done", [])]

class ActDrawCard(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["try_draw_card"])

    def process(self, game: ArkState, effect: str, args):
        # if a player tries to draw a card when that is valid, draw a card
        if game.sub_turn == ArkTurn.ACT and args[0] == game.turn:
            return [("draw_card", []), ("act_draw_card", [])]

class DrawCard(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["draw_card"])

    def process(self, game: ArkState, effect: str, args):
        # draw a card for the {args[0]}
        card = game.field.stack.draw()

        card.owner = args[0]
        game.field.hands[card.owner].add(card)

        return [("drawn_card", card)]



"""
class TouchMoveRule(Rule):
    def __init__(self, consequence: str, cause: str = "touch"):
        Rule.__init__(self, watch=[cause])

        self.prev = None
        self.cause = cause
        self.consequence = consequence

    def process(self, game: ArkState, effect: str, args):
        if effect == self.cause:
            if game.get_turn() not in args[1]:
                return

            piece = game.get_board().get_tile(args[0]).get_piece()

            if self.prev:
                prev, self.prev = self.prev, None

                m1, m2 = prev[0], args[0]
                p = prev[1]
                return [("select", prev), (self.consequence, (m1, m2, p))]
            elif piece:
                self.prev = args
                return [("select", args)]

            return []
"""