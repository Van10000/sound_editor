from ConsoleSoundEditor.CommandExecutor import CommandExecutor
from ConsoleSoundEditor.ConsoleModel import ConsoleModel


if __name__ == "__main__":
    console_model = ConsoleModel()
    executor = CommandExecutor(console_model)
    while True:
        executor.execute(input())
        if executor.is_finished:
            break
