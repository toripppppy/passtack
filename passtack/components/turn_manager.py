from components.command import Command
from components.player import Player
from components.damage import Damage


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


class TurnManager:
  """
  ターンごとに初期化され呼び出される
  player_A, player_B: プレイヤー
  turn: 今回のターンを指定(変更しない)
  """
  def __init__(self, player_A: Player, player_B: Player, turn: int) -> None:
    self.turn = turn

    # 一旦この仕様で
    self.player_A = player_A
    self.player_B = player_B

    self.player_A_action = Action(self.player_A, self.get_command_from_player(player_A, self.turn))
    self.player_B_action = Action(self.player_B, self.get_command_from_player(player_B, self.turn))

    # ターン終了後に発生させるイベント
    self.event_queue: list[Damage] = []

    # ターンの終了を判断する
    self.is_finished = False

  def get_command_from_player(self, player: Player, turn: int) -> Command:
    command = player.commands[turn - 1]
    return command
  
  def get_other_player(self, player: Player) -> Player:
    if player == self.player_A:
      return self.player_B
    else:
      return self.player_A
  
  def sort_actions(self, actions: list[Action]) -> list[Action]:
    # 処理順にソートする
    order = ["guess","trap","big_attack","attack","concentrate"]
    actions.sort(key=lambda action: order.index(action.command.name))
    return actions
  
  def append_event_queue(self, event) -> None:
    self.event_queue.append(event)

  def do_turn(self):
    actions = self.sort_actions([self.player_A_action, self.player_B_action])
    print(list(map(lambda x: x.command.name, actions)))
    
    ### これで全25通り網羅できます！！！！！
    # ======================================== #

    # 先攻
    def action_1():
      ### 推理
      # 相手のコマンド : trap || attack || big_attack || concentrate
      if actions[0].command.name == "guess":
        guessed_command = input("コマンドを予想してください: ")

        if guessed_command == actions[1].command.name:
          print("推理成功！")
          # 相手に１ダメージ、相手の攻撃はキャンセル（集中を除く）
          if actions[1].command.name != "concentrate":
            self.is_finished = True
          return Damage(1, source=actions[0].player, target=actions[1].player)
        
        else:
          print("推理失敗・・・")
          return Damage(0)

      ### トラップ
      # 相手のコマンド : attack || big_attack || concentrate
      if actions[0].command.name == "trap":
        if actions[1].command.name == "big_attack":
          print("トラップ発動！")
          return Damage(2, source=actions[0].player, target=actions[1].player)
        else:
          print("トラップは不発でした。")
          return Damage(0)
      
      ### 大攻撃
      # 相手のコマンド : attack || concentrate
      if actions[0].command.name == "big_attack":
        print("大攻撃！")

        # 攻撃に半分相殺される
        if actions[1].command.name == "attack":
          # 後攻を発動
          action_2()
          return Damage(1, source=actions[0].player, target=actions[1].player)
        
        # 通常通り2ダメージ
        else:
          return Damage(2, source=actions[0].player, target=actions[1].player)

      ### 攻撃
      # 相手のコマンド : concentrate
      if actions[0].command.name == "attack":
        print("攻撃！")
        return Damage(1, source=actions[0].player, target=actions[1].player)

    # 後攻
    def action_2():
      ### トラップ
      # 相手のコマンド : attack || big_attack || concentrate
      if actions[1].command.name == "trap":
        if actions[0].command.name == "big_attack":
          print("トラップ発動！")
          return Damage(2, source=actions[1].player, target=actions[0].player)
        else:
          print("トラップは不発でした。")
          return Damage(0)
      
      ### 大攻撃
      # 相手のコマンド : attack || concentrate
      if actions[1].command.name == "big_attack":
        print("大攻撃！")
        print("疲れた！休憩")
        return Damage(2, source=actions[1].player, target=actions[0].player)
      
      ### 攻撃
      # 相手のコマンド : concentrate
      if actions[1].command.name == "attack":
        print("攻撃！")
        if actions[0].command.name == "big_attack":
          print("半分を相殺しました。")
          self.is_finished = True
          return
        else:
          return Damage(1, source=actions[1].player, target=actions[0].player)

      ### 集中
      if actions[1].command.name == "concentrate":
        print("集中します")
        print(f"見えた！相手の次の行動は[{self.get_command_from_player(actions[0].player, self.turn + 1).name}]でした。")
        next_action = input("次のコマンドを入力してください:")
        print(f"次のコマンドを[{next_action}]にしました")
        return Damage(0)
      
    ### コマンドが被ると相殺される
    if actions[0].command.name == actions[1].command.name:
      print("相殺しました。")
    else:
      damage_1 = action_1()
      self.append_event_queue(damage_1)
      if self.is_finished == False:
        damage_2 = action_2()
        self.append_event_queue(damage_2)
    # ======================================== #

