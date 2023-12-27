from components.player import Player

class Damage:

  def __init__(self, amount: int, source: Player = None, target: Player = None) -> None:
    self.amount = amount
    self.source = source
    self.target = target



# ダメージの相殺分を調整
def adjust_damage(damage_A: Damage, damage_B: Damage) -> Damage:
  if damage_A.amount == damage_B.amount:
    return Damage(0)
  
  if damage_A.amount > damage_B.amount:
    new_amount = damage_A.amount - damage_B.amount
    return Damage(new_amount, source=damage_A.source, target=damage_A.target)
  
  if damage_A.amount < damage_B.amount:
    new_amount = damage_B.amount - damage_A.amount
    return Damage(new_amount, source=damage_B.source, target=damage_B.target)