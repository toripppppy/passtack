class Command:
  """
  name: 名前
  is_active: 2ターンの管理に使う
  """
  def __init__(self, name: str) -> None:
    self.name = name
    self.is_active = True

  def set_active(self, state) -> None:
    self.is_active = state