
"""Rules that control the turn structure"""

from chess.rules.rules import Rule, cause
from chess.structures.ark.struct import ArkAction, ArkState, ArkTurn, ArkPhase, ArkPlayer

class Init(Rule):
    """Initialize the game"""

    def __init__(self):
        Rule.__init__(self, watch=["init"])

    def process(self, game: ArkState, effect: str, args):
        return cause("init_turn")


class TurnNext(Rule):
    """If the current turn has ended, but the game is not over yet,
    signal the start of the next turn"""

    def __init__(self):
        Rule.__init__(self, watch=["turn_end"])

    def process(self, game: ArkState, effect: str, args):
        if game.phase != ArkPhase.END:
            game.turn_num += 1
            return cause("turn_next")


class PassiveDPGain(Rule):
    """Gain DP passively each turn"""

    DP = {ArkPhase.EARLY: 2, ArkPhase.MID: 4, ArkPhase.LATE: 100, ArkPhase.END: 0}

    def __init__(self):
        Rule.__init__(self, watch=["init_turn"])

    def process(self, game: ArkState, effect: str, args):
        ddp = PassiveDPGain.DP[game.phase]
        eff = []

        for player in ArkPlayer:
            game.field.dp[player] += ddp
            eff += cause("gfx_update_dp", player)

        return eff

class InitSubturn(Rule):
    """TODO prepare the next sub turn"""

    def __init__(self):
        Rule.__init__(self, watch=["init_subturn"])

    def process(self, game: ArkState, effect: str, args):
        eff = cause("can_move_check")

        if game.subturn == ArkTurn.ACT:
            game.actions_remaining = 2
            eff += cause("gfx_update_act")

        if game.subturn == ArkTurn.MOVE:
            eff += cause("init_move")

        return eff


class InitAction(Rule):
    """Prepare the next action"""

    def __init__(self):
        Rule.__init__(self, watch=["init_action"])

    def process(self, game: ArkState, effect: str, args):
        if game.subturn == ArkTurn.ACT:
            action = args[0]

            if action == game.last_action and action != ArkAction.DRAW:
                return

            if action == ArkAction.DEPLOY:
                game.action = action
                game.sub_actions_remaining = 3
            
            elif action == ArkAction.ENERGY and game.energy_valid:
                game.action = action
                game.sub_actions_remaining = game.get_energy_flux()

            elif action == ArkAction.RETREAT:
                game.action = action
                game.sub_actions_remaining = 10

            return cause("gfx_update_sub_act")

class TrySkipSubturn(Rule):
    """Tries to skip the subturn"""

    def __init__(self):
        Rule.__init__(self, watch=["try_skip_subturn"])

    def process(self, game: ArkState, effect: str, args):
        if (game.turn == args[0]):
            return cause("skip_subturn")

class SkipSubturn(Rule):
    """Allow the (forceful) skipping of subturns"""

    def __init__(self):
        Rule.__init__(self, watch=["skip_subturn"])

    def process(self, game: ArkState, effect: str, args):
        if game.subturn == ArkTurn.ACT:
            if (game.action == ArkAction.NONE):
                return cause("player_act_done")
            elif (game.action == ArkAction.DEPLOY):
                return cause("player_deploy_done")
            elif (game.action == ArkAction.ENERGY):
                return cause("player_energy_done")
            elif (game.action == ArkAction.RETREAT):
                return cause("player_retreat_done")
        elif game.subturn == ArkTurn.MOVE:
            return cause("player_move_done")
        elif game.subturn == ArkTurn.SKILL:
            return cause("player_skill_done")
        elif game.subturn == ArkTurn.COMBAT:
            return cause("player_combat_done")

class SkipAction(Rule):
    def __init__(self):
        Rule.__init__(self, watch=["player_deploy_done", "player_energy_done", "player_retreat_done"])
    
    def process(self, game: ArkState, effect: str, args):
        game.action = ArkAction.NONE
        return cause("player_subact_done") + cause("gfx_update_sub_act")

class SubturnNext(Rule):
    """TODO someone has ended their subturn, what's next?"""

    def __init__(self):
        Rule.__init__(self, watch=["player_act_done", "player_move_done",
                      "player_skill_done", "player_combat_done", "turn_next"])

    def process(self, game: ArkState, effect: str, args):
        if game.turn == ArkPlayer.DEFENDER:
            if effect == "player_act_done":
                game.last_action = ArkAction.NONE
                
            game.turn = ArkPlayer.ATTACKER
            return cause("init_subturn")

        if game.turn == ArkPlayer.ATTACKER:
            if effect == "player_act_done":
                game.last_action = ArkAction.NONE
                game.turn = ArkPlayer.DEFENDER
                game.subturn = ArkTurn.MOVE
                return cause("init_subturn")

            if effect == "player_move_done":
                game.turn = ArkPlayer.DEFENDER
                game.subturn = ArkTurn.SKILL
                return cause("init_subturn")

            if effect == "player_skill_done":
                game.turn = ArkPlayer.DEFENDER
                game.subturn = ArkTurn.COMBAT
                return cause("init_subturn")

            if effect == "player_combat_done":
                return cause("do_combat")

            if effect == "turn_next":
                game.turn = ArkPlayer.DEFENDER
                game.subturn = ArkTurn.ACT
                return cause("init_turn") + cause("init_subturn")


class CountAction(Rule):
    """Decrement the counter each action taken, and end the action subturn when it hits zero"""

    def __init__(self):
        Rule.__init__(self, watch=["act_draw_card", "player_subact_done"])

    def process(self, game: ArkState, effect: str, args):
        if game.actions_remaining > 1:
            game.actions_remaining -= 1
            return cause("gfx_update_act")
        else:
            return cause("player_act_done")


class CountSubaction(Rule):
    """Decrement the counter each subaction taken, and end the action when it hits zero"""

    def __init__(self):
        Rule.__init__(self, watch=["transact_play_card", "transact_promote"])

    def process(self, game: ArkState, effect: str, args):
        if game.sub_actions_remaining > 1:
            game.sub_actions_remaining -= 1
            return cause("gfx_update_sub_act")
        else:
            game.sub_actions_remaining = 0
            game.last_action = game.action
            game.action = ArkAction.NONE
            return cause("player_subact_done") + cause("gfx_update_sub_act")