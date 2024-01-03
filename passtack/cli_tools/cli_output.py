from components import Messager

class CLIOutput(Messager):
  def __init__(self) -> None:
    super().__init__()

  # オーバーライド
  def print(self, text) -> None:
    print(text)