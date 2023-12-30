from components.command import Command
from components.player import Player
from components.damage import Damage
from components.messager import Messager


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

    self.messager = Messager()

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
    # 後攻をキャンセルする
    def cancel_action_2() -> None:
      self.is_finished = True

    # 先攻
    def action_1() -> Damage:
      ### 推理
      # 相手のコマンド : trap || attack || big_attack || concentrate
      if actions[0].command.name == "guess":
        is_success = False

        # 攻撃はバレバレなので推理が必ず成功する仕様
        if actions[1].command.name == "attack":
          is_success = True
          self.messager.message("guess_attack")

        elif input("コマンドを予想してください: ") == actions[1].command.name:
          is_success = True

        if is_success:
          # 推理成功　相手に１ダメージ、相手の行動はキャンセル（集中を除く）
          damage = Damage(1, source=actions[0].player, target=actions[1].player)
          self.messager.message("guess_success")
          self.messager.cancel(actions[1])
          self.messager.damage(damage)
          if actions[1].command.name != "concentrate":
            cancel_action_2()
        else:
          # 推理失敗　何も起こらない
          self.messager.message("guess_failure")
          damage = Damage(0)

        return damage
            
      ### トラップ
      # 相手のコマンド : attack || big_attack || concentrate
      if actions[0].command.name == "trap":
        if actions[1].command.name == "big_attack":
          # トラップ成功　相手に２ダメージ、相手の大攻撃はキャンセル
          damage = Damage(2, source=actions[0].player, target=actions[1].player)
          self.messager.message("trap_success")
          self.messager.damage(damage)
          cancel_action_2()
        else:
          # トラップ失敗　何も起こらない
          damage = Damage(0)
          self.messager.message("trap_failure")
        
        return damage
      
      ### 大攻撃
      # 相手のコマンド : attack || concentrate
      if actions[0].command.name == "big_attack":
        self.messager.message("big_attack")

        # 攻撃に半分相殺される
        if actions[1].command.name == "attack":
          damage = Damage(1, source=actions[0].player, target=actions[1].player)
          self.messager.message("set_off_harf")
          cancel_action_2()
        
        # 通常通り2ダメージ
        else:
          damage = Damage(2, source=actions[0].player, target=actions[1].player)

        self.messager.damage(damage)
        self.messager.message("big_attack_sleep")
        return damage

      ### 攻撃
      # 相手のコマンド : concentrate
      if actions[0].command.name == "attack":
        print("攻撃！")
        return Damage(1, source=actions[0].player, target=actions[1].player)

    # 後攻
    def action_2() -> Damage:
      ### トラップ
      # 相手のコマンド : guess
      if actions[1].command.name == "trap":
        # 相手のコマンドは guess しかないので必ず失敗する
        damage = Damage(0)
        self.messager.message("trap_failure")
        return damage
      
      ### 大攻撃
      # 相手のコマンド : guess
      if actions[1].command.name == "big_attack":
        damage = Damage(2, source=actions[1].player, target=actions[0].player)
        self.messager.message("big_attack")
        self.messager.damage(damage)
        self.messager.message("big_attack_sleep")
        return damage
      
      ### 攻撃
      # 相手のコマンド : trap
      if actions[1].command.name == "attack":
        damage = Damage(1, source=actions[1].player, target=actions[0].player)
        self.messager.message("attack")
        self.messager.damage(damage)
        return damage

      ### 集中
      # 相手のコマンド : guess || trap || big_attack || attack
      if actions[1].command.name == "concentrate":
        self.messager.message("concentrate_start")
        if actions[0].command.name == "big_attack":
          # 次のターンは空白でそのショックから動けなくなる仕様
          self.messager.message("big_attack_sleep")
        else:
          self.messager.concentrate(self.get_command_from_player(actions[0].player, self.turn + 1).name)
          
          # TODO コマンドの入力を受けてActionを生成する
          next_action = input("次のコマンドを入力してください:")
          print(f"次のコマンドを[{next_action}]にしました")
        return Damage(0)
      
    ### コマンドが被ると相殺される
    if actions[0].command.name == actions[1].command.name:
      self.messager.message("set_off")
    else:
      damage_1 = action_1()
      self.append_event_queue(damage_1)
      if self.is_finished == False:
        damage_2 = action_2()
        self.append_event_queue(damage_2)
    # ======================================== #

