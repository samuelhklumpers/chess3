"""The rules for displaying things for Arkbruh"""

from chess.rules.rules import Rule
from chess.structures.ark.struct import ArkState, ArkPlayer


class Refresh(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["init", "connect"])

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

        print(args[0], "Hand:", game.field.hands[args[0]])

        for card in game.field.hands[args[0]].cards:
            # TODO implement json for ArkPlayer and ArkCard
            eff.append(("send_update_hand", [args[0], card]))

        return eff

class UpdateAct(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["gfx_update_act"])

    def process(self, game: ArkState, effect: str, args):
        print("Acts remaining:", game.actions_remaining)
      
        return [("send_update_act", ["all", game.actions_remaining])]

class UpdateSubact(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["gfx_update_sub_act"])

    def process(self, game: ArkState, effect: str, args):
        print("Sub actions remaining:", game.sub_actions_remaining, game.action)
      
        return [("send_update_sub_act", ["all", game.sub_actions_remaining, game.action])]

class UpdateDP(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["gfx_update_dp"])

    def process(self, game: ArkState, effect: str, args):
        print("DP", args[0], ":",  game.field.dp[args[0]])
      
        return [("send_update_dp", ["all", (args[0], game.field.dp[args[0]])])]

class UpdateTurn(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["gfx_update_turn"])

    def process(self, game: ArkState, effect: str, args):
        print("Turn", game.turn_num, ":", game.turn, "/", game.subturn)
      
        return [("send_update_turn", ["all", game.turn_num, game.turn, game.subturn])]

class UpdateTile(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["gfx_update_tile"])

    def process(self, game: ArkState, effect: str, args):
        print("Tile now looks like:", args[0])
      
        tile_info = tile_c = None

        return [("send_update_tile", ["all", tile_info, tile_c])]
