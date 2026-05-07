from typing import ClassVar

from cmd import MoveRobotCmd, TurnRobotCmd, SetToolRobotCmd, StartRobotCmd, StopRobotCmd
from robot import Robot


# интерпретатор команд
# интерпретирует построчно
# игнорирует пустые строки
# продолжает работать если команда неверная или с ошибкой

class Interpreter:
    COMMANDS: ClassVar[dict[str, type]] = {
        MoveRobotCmd.name: MoveRobotCmd,
        TurnRobotCmd.name: TurnRobotCmd,
        SetToolRobotCmd.name: SetToolRobotCmd,
        StartRobotCmd.name: StartRobotCmd,
        StopRobotCmd.name: StopRobotCmd,
    }

    def __init__(self, robot: Robot):
        self._robot = robot

    def run_line(self, line: str):
        parts = line.split()

        # игнорируем пустые строки
        if not parts:
            return

        cmd_name = parts[0]
        args = parts[1:]

        cmd_cls = self.COMMANDS.get(cmd_name)
        if cmd_cls is None:
            print("Неизвестная команда")
            return

        try:
            cmd = cmd_cls.from_args(args)
            cmd.do(self._robot)
        except Exception as e:
            print("неправильный формат / ошибка выполнении команды -> " + line)

    def run(self, program: list[str]):
        for line in program:
            self.run_line(line)
