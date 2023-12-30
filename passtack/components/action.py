from components.player import Player
from components.command import Command

class Action:  
  """
  プレイヤーのコマンド使用を、プレイヤーとコマンドを紐づけたActionとして扱う
  player: 使用するプレイヤー
  command: 使用されるコマンド
  """
  def __init__(self, player: Player, command: Command) -> None:
    self.player = player
    self.command = command
    pass