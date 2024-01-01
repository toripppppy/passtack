from components import Player, Command, TurnManager, Damage, Messager, InputManager

input_manager = InputManager()

# 行先未定
def convert_to_commands(stack: list[str]):
  commands = list()
  for command_name in stack:
    commands.append(Command(command_name))
    if command_name in ["big_attack","concentrate"]:
      commands.append(Command(command_name, is_active=False))

  return commands

input_manager.get_stack_input()

player_A = Player("A", convert_to_commands(input_manager.commands))
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
  tm = TurnManager(player_A, player_B, i)
  tm.do_turn()

  for event in tm.event_queue:
    if isinstance(event, Damage):
      print(event)
      apply_damage(event)



print(f"[{player_A.name}] 総被ダメージ: {player_A.damage_count}")
print(f"[{player_B.name}] 総被ダメージ: {player_B.damage_count}")