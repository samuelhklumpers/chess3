from rules.rules import *
from structures.ark.struct import *
from structures.ark.cards import *


class Refresh(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["init"])

    def process(self, game: ArkState, effect: str, args):
        eff = [("gfx_update_act", []), ("gfx_update_turn", [])]

        for player in ArkPlayer:
            eff.append(("gfx_update_hand", [player]))
        
        return eff

class UpdateHand(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["gfx_update_hand"])

    def process(self, game: ArkState, effect: str, args):
        eff = []

        for card in game.field.hands[args[0]].cards:
            # TODO implement json for ArkPlayer and ArkCard
            eff.append(("send_update_hand", [args[0], card]))

        return eff

class UpdateAct(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["gfx_update_act"])

    def process(self, game: ArkState, effect: str, args):
        return [("send_update_act", ["all", game.acts_remaining])]

class UpdateTurn(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["gfx_update_turn"])

    def process(self, game: ArkState, effect: str, args):
        return [("send_update_turn", ["all", game.turn_num, game.turn, game.sub_turn])]

