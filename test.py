from server.ark_setup import *

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
