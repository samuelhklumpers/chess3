"""Rules for the Action subturn"""

from chess.rules.rules import Rule, cause
from chess.structures.ark.struct import ArkState, ArkTurn, ArkPlayer, ArkTerrain, ArkAction


class ActDrawCard(Rule):
    """Check if the player is allowed to draw a card"""

    def __init__(self):
        Rule.__init__(self, watch=["try_draw_card"])

    def process(self, game: ArkState, effect: str, args):
        if game.subturn == ArkTurn.ACT and game.action == ArkAction.NONE and args[0] == game.turn:
            game.last_action = ArkAction.DRAW

            return cause("draw_card", *args) + cause("act_draw_card")


class PlaceUnitFromHand(Rule):
    """Check if the player is allowed to play a card from their hand"""

    def __init__(self):
        Rule.__init__(self, watch=["input_place_unit_from_hand"])

    def process(self, game: ArkState, effect: str, args):
        (player, card_i, tile_c) = args

        if not (game.action == ArkAction.DEPLOY and player == game.turn):
            return

        if card_i >= len(game.field.hands[player].cards):
            return

        tile = game.field.board.get_tile(tile_c)
        card = game.field.hands[player][card_i]

        if tile and game.field.dp[player] > card.cost:
            return cause("place_unit", (cause("transact_play_card", player, tile, card_i), []), player, tile, card)


class PromoteCardRule(Rule):
    """Check if the player is allowed to promote a card"""

    def __init__(self):
        Rule.__init__(self, watch=["input_promote_unit"])

    def process(self, game: ArkState, effect: str, args):
        (player, card) = args

        if not (game.action == ArkAction.DEPLOY and player == game.turn):
            return

        if game.field.dp[player] >= card:
            return cause("promote_unit",
                    [(cause("transact_promote", player, card), []), args])


class DrawCard(Rule):
    """Draw a card for the target"""

    def __init__(self):
        Rule.__init__(self, watch=["draw_card"])

    def process(self, game: ArkState, effect: str, args):
        card = game.field.stack.draw()

        card.owner = args[0]
        game.field.hands[card.owner].add(card)

        return cause("drawn_card", card, *args) + cause("gfx_update_hand", *args)


class PlaceUnit(Rule):
    """Try to place a unit"""

    Ok = {ArkPlayer.ATTACKER: [ArkTerrain.SPAWN],
          ArkPlayer.DEFENDER: [ArkTerrain.NORMAL, ArkTerrain.HIGH]}

    def __init__(self):
        Rule.__init__(self, watch=["place_unit"])

    def process(self, game: ArkState, effect: str, args):
        ((onsuccess, onfail), player, tile, card) = args

        if tile.terrain not in PlaceUnit.Ok[player]:
            return onfail

        if tile.terrain == ArkTerrain.HIGH and card.position not in ["ranged", "flying"]:
            return onfail

        if len(tile.cards) > 1:
            return onfail

        tile.cards.append(card)

        # to do: pushing

        return onsuccess + cause("gfx_update_tile", tile)


class PromoteUnit(Rule):
    """Promote a unit"""

    def __init__(self):
        Rule.__init__(self, watch=["promote_unit"])

    def process(self, game: ArkState, effect: str, args):
        # ((onsuccess, onfail), (player, card_i, tile_c)) = args
        # to do: everything
        tile = None

        return cause("gfx_update_tile", tile)


class TransactPlayCard(Rule):
    """When a card has been succesfully played,
    remove it from the player's hand and deduct the cost from their DP"""

    def __init__(self):
        Rule.__init__(self, watch=["transact_play_card"])

    def process(self, game: ArkState, effect: str, args):
        (player, _, card_i) = args

        card = game.field.hands[player].cards.pop(card_i)
        game.field.dp[player] -= card.cost

        return [("gfx_update_hand", args), ("gfx_update_dp", args), ("played_unit", args)]


# class PlayedUnit(Rule):
#     def __init__(self):
#         Rule.__init__(self, watch=["played_unit"])

#     def process(self, game: ArkState, effect: str, args):
#         ...

#         return [("gfx_update_hand", args), ("gfx_update_dp", args), ("played_unit", args)]