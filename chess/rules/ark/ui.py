from chess.rules.rules import Rule, cause
from chess.structures.ark.struct import ArkState, ArkTurn, ArkPlayer, ArkTerrain, ArkAction


class UserClickUnit(Rule):
    def __init__(self):
        Rule.__init__("input_click_unit")

    def process(self, game: ArkState, effect: str, args):
        (player, unit, tile) = args

        if game.subturn == ArkTurn.MOVE and game.turn == player:
            if player == unit.owner:
                game.selected_unit = (unit, tile)


class UserClickTile(Rule):
    def __init__(self):
        Rule.__init__("input_click_tile")

    def process(self, game: ArkState, effect: str, args):
        (player, tile2) = args

        if game.subturn == ArkTurn.MOVE and game.turn == player:
            if game.selected_unit is not None:
                (unit, tile1) = game.selected_unit
                return cause("input_move_unit", unit, tile1, tile2)
