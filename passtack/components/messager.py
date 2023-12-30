from components.action import Action
from components.damage import Damage

import json
import re

class Messager:
  def __init__(self) -> None:
    self.json_path = "passtack/src/json/turn_message.json"

  def get_json(self) -> object:
    json_open = open(self.json_path, 'r')
    return json.load(json_open)

  def get_message_template(self, key: str) -> str:
    j = self.get_json()
    if key in j.keys():
      return j[key]
    
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
    self.message("concentrate_start")
    
    msgtmp = self.get_message_template("concentrate_seen")
    print(msgtmp.format(
      player=seen_action.player.name,
      command=seen_action.command.name,
    ))
