from components import Command
import inquirer

# サイン -> コマンドへの対応表
command_dict = {
  "attack": {
    "sign": ".",
    "description": "[.]攻撃",
    "turn_amount": 1
  },
  "big_attack": {
    "sign": ",",
    "description": "[,]大攻撃",
    "turn_amount": 2
  },
  "concentrate": {
    "sign": "*",
    "description": "[*]集中",
    "turn_amount": 2
  },
  "trap": {
    "sign": "_",
    "description": "[_]トラップ",
    "turn_amount": 1
  },
  "guess": {
    "sign": "?",
    "description": "[?]推理",
    "turn_amount": 1
  },
}

class CLIInput:
  """
  CLI的に入力を取得するUI
  使い捨てが前提
  """
  def __init__(self, turn_limit) -> None:
    self.commands = list()
    self.turn_limit = turn_limit
  
  def get_command_input(self) -> Command:
    self.get_command_stack_input()
    return self.convert_to_command_stack(self.commands)[0]

  def get_command_stack_input(self) -> list[Command]:
    self.name_stack_input()
    return self.convert_to_command_stack(self.commands)

  # スタックの入力を受け付ける
  def name_stack_input(self):
    self.sign_input()

    if self.calc_using_turns() < self.turn_limit:
      # 再帰
      self.name_stack_input()
      return

    print(self.create_command_display())
    self.name_stack_input_finish()

  def name_stack_input_finish(self):
    fix_stack = self.confirm("以上で決定しますか？")
    if fix_stack:
      print("決定しました。")
      # debug
      # print(self.commands)
    else:
      print("再度選択してください。")
      # 初期化してやり直し
      self.__init__(self.turn_limit)
      self.name_stack_input()

  # サインの入力を受け付ける
  def sign_input(self):
    # 表示
    print()
    print(self.create_command_display())

    choices = list()
    for cmd in command_dict.values():
      # 残りターンに応じて使用可能なコマンドのみを選択肢に追加する
      if cmd["turn_amount"] <= self.calc_remaining_turns():
        choices.append(cmd["description"])
    
    # 入力の受け付け
    answer = self._list(
        message="コマンドを選択してください",
        choices=choices
      )
    self.commands.append(self.get_key_by_description(answer))

  def convert_to_command_stack(self, name_stack: list[str]) -> list[Command]:
    commands = list()
    for command_name in name_stack:
      commands.append(Command(command_name))
      if command_name in ["big_attack","concentrate"]:
        commands.append(Command(command_name, is_active=False))

    return commands

  # command_dict を description で逆引きする
  def get_key_by_description(self, description: str) -> str:
    key_dict = {v["description"] : k for k, v in zip(command_dict.keys(), command_dict.values())}
    return key_dict[description]

  # ./././-/-[3/5] のような表示を作成する
  def create_command_display(self) -> str:
    commands = list()
    for command in self.commands:
      commands.append(command_dict[command]["sign"])

    # 隙間埋め
    commands += ["-"] * self.calc_remaining_turns()

    return "/".join(commands) + f"[{self.calc_using_turns()}/{self.turn_limit}]"
  
  # 使用中のターン数を計算する
  def calc_using_turns(self) -> int:
    turns = 0
    for command in self.commands:
      turns += command_dict[command]["turn_amount"]

    return turns
  
  def calc_remaining_turns(self) -> int:
    return self.turn_limit - self.calc_using_turns()
  
  def _list(self, message: str, choices: list[str]) -> str:
    questions = [
      inquirer.List("_",
      message=message,
      choices=choices
      ),
    ]
    answers = inquirer.prompt(questions)
    return answers["_"]

  def confirm(self, message: str) -> bool:
    questions = [
      inquirer.List("_",
      message=message,
      choices=["Yes","No"]
      ),
    ]
    answers = inquirer.prompt(questions)
    return True if answers["_"] == "Yes" else False