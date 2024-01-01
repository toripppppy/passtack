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
    
  ### 汎用
  def message(self, key: str) -> None:
    msgtmp = self.get_message_template(key)
    # 変数の埋め込みが必要であればエラー
    if re.match(r"\{.*\}", msgtmp):
      raise f"Error: {key} requires format"
    print(msgtmp)
    
  def damage(self, damage: Damage) -> None:
    msgtmp = self.get_message_template("damage")
    print(msgtmp.format(
      source=damage.source.name,
      target=damage.target.name,
      amount=damage.amount,
    ))

  def cancel(self, target_action: Action) -> None:
    msgtmp = self.get_message_template("cancel")
    print(msgtmp.format(
      player=target_action.player.name,
      command=target_action.command.name,
    ))

  ### 固有
  def concentrate(self, seen_action: Action) -> None:
    self.message("concentrate.start")
    
    msgtmp = self.get_message_template("concentrate.seen")
    print(msgtmp.format(
      player=seen_action.player.name,
      command=seen_action.command.name,
    ))
