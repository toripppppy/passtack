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

class InputManager:
  def __init__(self) -> None:
    self.commands = list()

  # スタックの入力を受け付ける
  def get_stack_input(self):
    self.get_sign_input()

    if self.calc_using_turns() < 5:
      # 再帰
      self.get_stack_input()
      return

    print(self.create_command_display())
    self.get_stack_input_finish()

  def get_stack_input_finish(self):
    fix_stack = self.confirm("以上で決定しますか？")
    if fix_stack:
      print("決定しました。")
      # debug
      print(self.commands)
    else:
      print("再度選択してください。")
      # 初期化してやり直し
      self.__init__()
      self.get_stack_input()

  # サインの入力を受け付ける
  def get_sign_input(self):
    # 表示
    print()
    print(self.create_command_display())

    remaining_turns = 5 - self.calc_using_turns()
    choices = list()
    for cmd in command_dict.values():
      # 残りターンに応じて使用可能なコマンドのみを選択肢に追加する
      if cmd["turn_amount"] <= remaining_turns:
        choices.append(cmd["description"])
    
    # 入力の受け付け
    answer = self._list(
        message="コマンドを選択してください",
        choices=choices
      )
    self.commands.append(self.get_key_by_description(answer))

  # command_dict を description で逆引きする
  def get_key_by_description(self, description: str) -> str:
    key_dict = {v["description"] : k for k, v in zip(command_dict.keys(), command_dict.values())}
    return key_dict[description]

  # ./././-/-[3/5] のような表示を作成する
  def create_command_display(self) -> str:
    commands = list()
    for command in self.commands:
      commands.append(command_dict[command]["sign"])

    remaining_turns = 5 - self.calc_using_turns()

    commands += ["-"]*remaining_turns

    return "/".join(commands) + f"[{self.calc_using_turns()}/5]"
  
  # 使用中のターン数を計算する
  def calc_using_turns(self) -> int:
    turns = 0
    for command in self.commands:
      turns += command_dict[command]["turn_amount"]

    return turns
  
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