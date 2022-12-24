"""The basic rules for Arkbruh"""

from chess.rules.rules import Rule, cause
from chess.structures.ark.struct import ArkState


class WinCheck(Rule):
    """TODO check if someone has won"""

    def __init__(self):
        Rule.__init__(self, watch=["combat_done"])

    def process(self, game: ArkState, effect: str, args):
        if effect == "combat_done":
            return cause("turn_end", effect)


class CanMoveCheck(Rule):
    """If the player cannot perform a move, skip their subturn"""

    def __init__(self):
        Rule.__init__(self, watch=["can_move_check"])

    def process(self, game: ArkState, effect: str, args):
        if not game.has_valid(game.turn, game.subturn):
            return cause("skip_subturn")
        else:
            return cause("gfx_update_turn")


class DoCombat(Rule):
    """TODO process the combat queue"""

    def __init__(self):
        Rule.__init__(self, watch=["do_combat"])

    def process(self, game: ArkState, effect: str, args):
        return cause("combat_done")
