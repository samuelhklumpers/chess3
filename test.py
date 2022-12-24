"""Test drawing cards"""

from chess.server.ark_setup import setup_ark
from chess.structures.ark.struct import ArkPlayer

game = setup_ark()

print()
game.ruleset.process("try_draw_card", [ArkPlayer.DEFENDER])
print()
game.ruleset.process("try_draw_card", [ArkPlayer.DEFENDER])
print()
game.ruleset.process("try_draw_card", [ArkPlayer.ATTACKER])
print()
game.ruleset.process("try_draw_card", [ArkPlayer.ATTACKER])
print()

game.ruleset.process("try_draw_card", [ArkPlayer.DEFENDER])
print()
game.ruleset.process("try_draw_card", [ArkPlayer.DEFENDER])
print()
game.ruleset.process("try_draw_card", [ArkPlayer.ATTACKER])
print()
game.ruleset.process("try_draw_card", [ArkPlayer.ATTACKER])
