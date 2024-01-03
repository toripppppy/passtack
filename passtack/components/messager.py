from components.action import Action
from components.damage import Damage

import json
import re

class Messager:
  def __init__(self) -> None:
    self.json_path = "passtack/src/json/messager.jsonc"
    self.json_data = self.get_json_data()

  def get_json_data(self) -> object:
    with open(self.json_path, 'r', encoding='utf-8') as f:
      jsonc_text = f.read()
    json_text = self.delete_comments(jsonc_text)
    return json.loads(json_text)
  
  def delete_comments(self, text: str) -> str:
    re_text = re.sub(r'/\*[\s\S]*?\*/|//.*', '', text)
    return re_text

  def get_message_template(self, key: str) -> str:
    json_data = self.json_data
    if key in json_data.keys():
      return json_data[key]
    
  def print(self, text) -> None:
    print("<print> please override")

  def wait(self) -> None:
    print("<wait> please override")

  def clear(self) -> None:
    print("<clear> please override")
    
  ### 汎用
  def message(self, key: str) -> None:
    msgtmp = self.get_message_template(key)
    # 変数の埋め込みが必要であればエラー
    if re.match(r"\{.*\}", msgtmp):
      raise f"Error: {key} requires format"
    self.print(msgtmp)
    
  def message_with_damage(self, damage: Damage) -> None:
    msgtmp = self.get_message_template("damage")
    self.print(msgtmp.format(
      source=damage.source.name,
      target=damage.target.name,
      amount=damage.amount,
    ))

  def message_with_action(self, key: str, action: Action) -> None:
    msgtmp = self.get_message_template(key)
    self.print(msgtmp.format(
      player=action.player.name,
      command=action.command.name,
    ))

  def message_with_turn(self, key: str, turn: int):
    msgtmp = self.get_message_template(key)
    self.print(msgtmp.format(turn=turn))

  ### 固有
  def cancel(self, target_action: Action) -> None:
    self.message_with_action("cancel", target_action)

  def concentrate(self, seen_action: Action) -> None:
    self.message_with_action("concentrate.seen", seen_action)

  def use_command(self, action: Action) -> None:
    self.message_with_action("use", action)