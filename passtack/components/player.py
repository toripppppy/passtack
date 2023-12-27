from components.command import Command

class Player:
  """
  name: 名前
  commands: 各ターンで使用するコマンド
  """
  def __init__(self, name: str, commands: list[Command] = None) -> None:
    self.name = name
    self.commands = commands
    self.damage_count = 0