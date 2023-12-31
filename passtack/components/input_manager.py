from components.command import Command

# サイン->コマンド名への変換表
convert_list = {
  ".": "attack",
  ",": "big_attack",
  "*": "concentrate",
  "_": "trap",
  "?": "guess",
}

class InputManager:
  def __init__(self) -> None:
    pass

  def get_sign_input(self) -> str:
    sign = input("sign: ")
    if sign in convert_list.keys():
      return sign
    else:
      # TODO messagerへの代替
      print("サインの形式が不適です。")
      # 再帰
      sign = self.get_sign_input()
      return sign
    
  def sign_to_command_name(self, sign: str) -> str:
    if sign in convert_list.keys():
      return convert_list[sign]
    else:
      raise f"Passtack Error: sign '{sign}' not found."

  def get_command(self) -> Command:
    command_name = self.sign_to_command_name(self.get_sign_input())
    return Command(name=command_name)