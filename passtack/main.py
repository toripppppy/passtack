from components import Player, Command, TurnManager, Damage


player_A = Player("A", [
  Command("guess"),
  Command("attack"),
  Command("attack"),
  Command("attack"),
  Command("attack"),
])
player_B = Player("B", [
  Command("trap"),
  Command("big_attack"),
  Command("concentrate"),
  Command("trap"),
  Command("guess"),
])

tm = TurnManager(player_A, player_B, 1)
tm.do_turn()

print(tm.event_queue)

def apply_damage(damage: Damage) -> None:
  if damage.amount == 0:
    return
  target_player = damage.target
  target_player.damage_count += damage.amount

for event in tm.event_queue:
  if isinstance(event, Damage):
    print(event)
    apply_damage(event)


print(f"[{player_A.name}] 総被ダメージ: {player_A.damage_count}")
print(f"[{player_B.name}] 総被ダメージ: {player_B.damage_count}")