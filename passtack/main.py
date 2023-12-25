from components import Player, Command, TurnManager


player_A = Player("A", [
  Command("attack"),
  Command("attack"),
  Command("attack"),
  Command("attack"),
  Command("attack"),
])
player_B = Player("B", [
  Command("big_attack"),
  Command("big_attack"),
  Command("concentrate"),
  Command("trap"),
  Command("guess"),
])

tm = TurnManager(player_A, player_B, 1)
tm.do_turn()