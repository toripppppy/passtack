from components import Player, Command, TurnManager, Damage
from input_manager import InputManager

player_A = Player("A", InputManager(turn_limit=5).get_command_stack_input())
player_B = Player("B", [
  Command("attack"),
  Command("big_attack"),
  # 休憩の挙動
  Command("big_attack", is_active=False),
  Command("trap"),
  Command("guess"),
])

# 行先未定 -> GameManager?
def apply_damage(damage: Damage) -> None:
  if damage.amount == 0:
    return
  target_player = damage.target
  target_player.damage_count += damage.amount

for i in range(1,5+1):
  tm = TurnManager(player_A, player_B, i, command_inputter=InputManager(turn_limit=1).get_command_input)
  tm.do_turn()

  for event in tm.event_queue:
    if isinstance(event, Damage):
      print(event)
      apply_damage(event)



print(f"[{player_A.name}] 総被ダメージ: {player_A.damage_count}")
print(f"[{player_B.name}] 総被ダメージ: {player_B.damage_count}")