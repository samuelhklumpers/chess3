import asyncio
import json
import websockets
from chess.rules.rules import Rule
from chess.structures.ark.cards import Card
from chess.structures.ark.struct import ArkPlayer, ArkState, ArkTurn


def encode_ark(o):
    if isinstance(o, Card):
        return o.__dict__
    elif isinstance(o, ArkPlayer):
        if o == ArkPlayer.ATTACKER:
            return "attacker"
        elif o == ArkPlayer.DEFENDER:
            return "defender"
    elif isinstance(o, ArkTurn):
        if o == ArkTurn.ACT:
            return "actions"
        elif o == ArkTurn.MOVE:
            return "movement"
        elif o == ArkTurn.SKILL:
            return "skills"
        elif o == ArkTurn.COMBAT:
            return "combat"

class ArkWebSocketRule(Rule):
    def __init__(self, game: ArkState, player: str, ws: websockets.WebSocketServerProtocol):
        Rule.__init__(self, ["send_update_hand", "send_update_act", "send_update_turn"])

        self.game = game
        self.ws = ws
        self.player = player

    def process(self, game: ArkState, effect: str, args):
        if args[0] in ["all", self.player]:
            out = json.dumps((effect, args[1:]), default=encode_ark)

            print("sending", out)

            asyncio.run_coroutine_threadsafe(self.ws.send(out), asyncio.get_event_loop())

    async def run(self):
        self.game.ruleset.process("connect", self.player)
        try:
            async for msg in self.ws:
                data = json.loads(msg)

                eff, arg = data

                # TODO update to include all user inputs
                if eff == "click":
                    self.game.ruleset.process("touch", (arg, self.player))
                elif eff == "draw":
                    self.game.ruleset.process("try_draw_card", [self.player])
        finally:
            self.game.ruleset.remove_rule(self)
            self.game.ruleset.process("disconnect", self.player)