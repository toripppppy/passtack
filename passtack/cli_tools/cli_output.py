from components import Messager

import os

class CLIOutput(Messager):
  def __init__(self) -> None:
    super().__init__()

  # オーバーライド
  def print(self, text) -> None:
    print(text)

  def wait(self) -> None:
    input("▶︎")

  def clear(self) -> None:
    os.system('clear')