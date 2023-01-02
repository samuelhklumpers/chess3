"""Rules that control unit movement"""

from chess.rules.rules import Rule, cause
from chess.structures.ark.struct import ArkAction, ArkState, ArkTurn, ArkPhase, ArkPlayer


class InitMove(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["init_move"])

    def process(self, game: ArkState, effect: str, args):
        player = game.turn

        for tile in game.field.board:
            for card in tile:
                if card.owner == player:
                    card.movements_remaining = -1


class MoveUnit(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["input_move_unit"])

    def process(self, game: ArkState, effect: str, args):
        (unit, tile1, tile2) = args
        eff = cause("gfx_update_unit", unit)
        
        dx = tile1.x - tile2.x
        dy = tile1.y - tile1.y

        if abs(dx) + abs(dy) > 1:
            return eff

        if game.last_moved_unit is not None and game.last_moved_unit != unit:
            game.last_moved_unit.movements_remaining = 0
            eff += cause("gfx_update_unit", game.last_moved_unit)

        if unit.movements_remaining == -1:
            if unit.owner == ArkPlayer.DEFENDER:
                if unit.position == "flying":
                    unit.movements_remaining = 1
                else:
                    unit.movements_remaining = 0
            else:
                unit.movements_remaining = unit.speed

        if unit.name == "scouting_drone":
            for unit2 in tile2:
                if unit.owner != unit2.owner:
                    return eff + cause("deselect_unit")

        if unit.movements_remaining > 0:
            if unit.heading != (dx, dy):
                unit.heading = (dx, dy)
                game.last_moved_unit = unit
            else:
                if len(tile2.cards) < 2:
                    for unit2 in tile2:
                        if unit.owner != unit2.owner and unit.name != "scouting_drone":
                            return eff

                    tile1.cards.remove(unit)
                    tile2.cards.append(unit)
                    game.last_moved_unit = unit

            unit.movements_remaining -= 1

            eff += cause("gfx_update_tile", tile1) + \
                cause("gfx_update_tile", tile2)

        if unit.movements_remaining == 0:
            eff += cause("deselect_unit")

        return eff
