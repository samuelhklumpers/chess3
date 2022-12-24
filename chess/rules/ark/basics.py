"""The basic rules for Arkbruh"""

from chess.rules.rules import Rule
from chess.structures.ark.struct import ArkState, ArkTurn, ArkPhase, ArkPlayer, ArkTerrain
#from structures.ark.cards


class WinCheck(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["combat_done"])

    def process(self, game: ArkState, effect: str, args):
        # TODO check if someone has won

        if effect == "combat_done":
            return [("turn_end", [effect])]

class TurnNext(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["turn_end"])

    def process(self, game: ArkState, effect: str, args):
        # if the current turn has ended, but the game is not over yet, signal the start of the next turn

        if game.phase != ArkPhase.END:
            game.turn_num += 1
            return [("turn_next", [])]

class InitSubturn(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["init_subturn"])

    def process(self, game: ArkState, effect: str, args):
        # TODO prepare the next sub turn

        if game.sub_turn == ArkTurn.ACT:
            game.acts_remaining = 2
            return [("gfx_update_act", []), ("can_move_check", [])]
        elif game.sub_turn == ArkTurn.MOVE:
            return [("can_move_check", [])]
        elif game.sub_turn == ArkTurn.SKILL:
            return [("can_move_check", [])]
        elif game.sub_turn == ArkTurn.COMBAT:
            return [("can_move_check", [])]

class CanMoveCheck(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["can_move_check"])

    def process(self, game: ArkState, effect: str, args):
        # if the player cannot perform a move, skip this sub turn
        if not game.has_valid(game.turn, game.sub_turn):
            # TODO unify subturn and sub_turn
            return [("skip_subturn", [])]
        else:
            return [("gfx_update_turn", [])]

class SkipSubturn(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["skip_subturn"])

    def process(self, game: ArkState, effect: str, args):
        if game.sub_turn == ArkTurn.ACT:
            return [("player_act_done", [])]
        elif game.sub_turn == ArkTurn.MOVE:
            return [("player_move_done", [])]
        elif game.sub_turn == ArkTurn.SKILL:
            return [("player_skill_done", [])]
        elif game.sub_turn == ArkTurn.COMBAT:
            return [("player_combat_done", [])]

class SubturnNext(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["player_act_done", "player_move_done", "player_skill_done", "player_combat_done", "turn_next"])

    def process(self, game: ArkState, effect: str, args):
        # TODO someone has ended their subturn, what's next?

        #print(game.turn, game.sub_turn)

        if game.turn == ArkPlayer.DEFENDER:
            game.turn = ArkPlayer.ATTACKER
            return [("init_subturn", [])]
        elif game.turn == ArkPlayer.ATTACKER:
            if effect == "player_act_done":
                game.turn = ArkPlayer.DEFENDER
                game.sub_turn = ArkTurn.MOVE
                return [("init_subturn", [])]
            elif effect == "player_move_done":
                game.turn = ArkPlayer.DEFENDER
                game.sub_turn = ArkTurn.SKILL
                return [("init_subturn", [])]
            elif effect == "player_skill_done":
                game.turn = ArkPlayer.DEFENDER
                game.sub_turn = ArkTurn.COMBAT
                return [("init_subturn", [])]
            elif effect == "player_combat_done":
                return [("do_combat", [])]
            elif effect == "turn_next":
                game.turn = ArkPlayer.DEFENDER
                game.sub_turn = ArkTurn.ACT
                return [("init_subturn", [])]

class DoCombat(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["do_combat"])

    def process(self, game: ArkState, effect: str, args):
        # TODO process the combat queue

        return [("combat_done", [])]

class CountAction(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["act_draw_card"])

    def process(self, game: ArkState, effect: str, args):
        # decrement the counter each action taken, and end the action subturn when it hits zero

        if game.acts_remaining > 1:
            game.acts_remaining -= 1
            return [("gfx_update_act", [])]
        else:
            return [("player_act_done", [])]

class ActDrawCard(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["try_draw_card"])

    def process(self, game: ArkState, effect: str, args):
        # if a player tries to draw a card when that is valid, draw a card
        if game.sub_turn == ArkTurn.ACT and args[0] == game.turn:
            return [("draw_card", args), ("act_draw_card", [])]

class DrawCard(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["draw_card"])

    def process(self, game: ArkState, effect: str, args):
        # draw a card for the {args[0]}
        card = game.field.stack.draw()

        card.owner = args[0]
        game.field.hands[card.owner].add(card)

        return [("drawn_card", [card]), ("gfx_update_hand", args)]

class PlayUnit(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["play_unit"])

    def process(self, game: ArkState, effect: str, args):
        ((onsuccess, onfail), (player, card_i, tile_c)) = args
        
        tile = game.field.board.get_tile(tile_c)
        card = game.field.hands[player][card_i]
            
        if player == ArkPlayer.ATTACKER and tile.terrain != ArkTerrain.SPAWN:
            return onfail
        elif player == ArkPlayer.DEFENDER and tile.terrain not in [ArkTerrain.NORMAL, ArkTerrain.HIGH]:
            return onfail
            
        if tile.terrain == ArkTerrain.HIGH and card.position not in ["ranged", "flying"]:
            return onfail

        if len(tile.cards) > 1:
            return onfail

        tile.cards.append(card)

        # TODO push
        
        return onsuccess + [("gfx_update_tile", tile)]

class TransactPlayUnit(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["transact_play_unit"])

    def process(self, game: ArkState, effect: str, args):
        (player, card_i, _) = args

        card = game.field.hands[player].cards.pop(card_i)
        game.field.dp[player] -= card.cost

        return [("gfx_update_hand", args), ("gfx_update_dp", args), ("played_unit", args)]

class PlayedUnit(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["played_unit"])

    def process(self, game: ArkState, effect: str, args):
        # TODO

        return [("gfx_update_hand", args), ("gfx_update_dp", args), ("played_unit", args)]
    

class PlayUnitFromHand(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["play_unit_from_hand"])

    def process(self, game: ArkState, effect: str, args):
        (player, card_i, tile_c) = args
        
        if not (game.sub_turn == ArkTurn.ACT and player == game.turn):
            return 
        
        if card_i >= len(game.field.hands[player]):
            return

        tile = game.field.board.get_tile(tile_c)
        card = game.field.hands[player][card_i]

        if tile and game.field.dp[player] > card.cost:
            return [("play_unit", (([("transact_play_unit", args)], []), args))]
                

# class PlayFromHand(Rule):
#     def __init__(self):
#         Rule.__init__(self, watch=["play_from_hand"])

#     def process(self, game: ArkState, effect: str, args):
#         ...
        
# class PlayFromHand(Rule):
#     def __init__(self):
#         Rule.__init__(self, watch=["play_from_hand"])

#     def process(self, game: ArkState, effect: str, args):
#         ...
        
# class PlayFromHand(Rule):
#     def __init__(self):
#         Rule.__init__(self, watch=["play_from_hand"])

#     def process(self, game: ArkState, effect: str, args):
#         ...
        
# class PlayFromHand(Rule):
#     def __init__(self):
#         Rule.__init__(self, watch=["play_from_hand"])

#     def process(self, game: ArkState, effect: str, args):
#         ...
        
# class PlayFromHand(Rule):
#     def __init__(self):
#         Rule.__init__(self, watch=["play_from_hand"])

#     def process(self, game: ArkState, effect: str, args):
#         ...
        
# class PlayFromHand(Rule):
#     def __init__(self):
#         Rule.__init__(self, watch=["play_from_hand"])

#     def process(self, game: ArkState, effect: str, args):
#         ...