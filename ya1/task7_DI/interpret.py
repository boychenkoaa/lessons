from robot import Robot
from robot_cmd import InterpreterCommandsDict, RobotCmd

# интерпретатор команд
# интерпретирует построчно
# игнорирует пустые строки
# продолжает работать если команда неверная или с ошибкой

class Interpreter:
    def __init__(self, robot: Robot, commands: InterpreterCommandsDict):
        self._robot = robot
        self._commands = commands

    @property
    def robot(self) -> Robot:
        return self._robot

    def run_line(self, line: str):
        parts = line.split()

        # игнорируем пустые строки
        if not parts:
            return

        cmd_name = parts[0]
        args = parts[1:]

        cmd_cls = self._commands.get(cmd_name)
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
