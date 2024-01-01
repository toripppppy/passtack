class Command:
  """
  name: 名前
  is_active: 2ターンの管理に使う
  """
  def __init__(self, name: str, is_active = False) -> None:
    self.name = name
    self.is_active = is_active
