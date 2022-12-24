"""Test drawing cards"""

from chess.server.ark_setup import setup_ark
from chess.structures.ark.struct import ArkAction, ArkPhase, ArkPlayer

game = setup_ark()
game.phase = ArkPhase.LATE
game.ruleset.debug = False

print("Drawing some cards...")
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
print()

print("Try to place some stuff")
game.ruleset.process("init_action", [ArkAction.DEPLOY])
print()
game.ruleset.process("input_place_unit_from_hand", [ArkPlayer.DEFENDER, 0, (0, 0)])
print()
game.ruleset.process("input_place_unit_from_hand", [ArkPlayer.DEFENDER, 0, (1, 0)])
print()
game.ruleset.process("input_place_unit_from_hand", [ArkPlayer.DEFENDER, 0, (2, 0)])
print()

print("Try to place more than you're allowed to...")
game.ruleset.process("input_place_unit_from_hand", [ArkPlayer.DEFENDER, 0, (3, 0)])
print()

print("Try to deploy twice...")
game.ruleset.process("init_action", [ArkAction.DEPLOY])
print()

print("Give up and draw a card instead")
game.ruleset.process("try_draw_card", [ArkPlayer.DEFENDER])
print()


