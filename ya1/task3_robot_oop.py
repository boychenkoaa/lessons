"""
Пока не буду расширяться сверх необходимого и оставлю свое первоначальное решение из задачи 1.
Оно как раз было в ООП-стиле.
"""

from enum import StrEnum
from math import radians, pi, degrees, sin, cos
from os import name
from typing import ClassVar, Self


class RobotTool(StrEnum):
    SOAP = "soap"
    WATER = "water"
    BRUSH = "brush"


Position = tuple[float, float]
Orientation = float

# класс робота -- отвечает непосредственно за действия самого робота

class Robot:
    def __init__(self):
        self._pos = (0.0, 0.0)
        self._orientation = 0.0
        self._tool = RobotTool.WATER

    def rotate(self, angle_rad: float):
        self._orientation = (self._orientation + angle_rad) % (2 * pi)

    def move(self, dist: float):
        dx = dist * cos(self._orientation)
        dy = dist * sin(self._orientation)
        self._pos = self._pos[0] + dx, self._pos[1] + dy

    @property
    def pos(self) -> Position:
        return self._pos

    @property
    def tool(self) -> RobotTool:
        return self._tool

    @property
    def orientation(self) -> Orientation:
        return self._orientation

# команда для робота
# более "высокоуровневая" чем метод самого робота 
# предобработка, логгирование, возможно комбинирование нескольких команд 
class RobotCmd:
    name:  ClassVar[str] = "unknown"

    def do(self, robot: Robot):
        raise NotImplementedError

    @classmethod
    def from_args(cls, args: list[str]) -> Self:
        raise NotImplementedError

# команда движения
class MoveRobotCmd:
    name:  ClassVar[str] = "move"

    def __init__(self, dist: float):
        self._dist = dist

    def do(self, robot: Robot):
        robot.move(self._dist)
        print(f"POS {robot.pos[0]:.2f}, {robot.pos[1]:.2f}")

    @classmethod
    def from_args(cls, args: list[str]):
        if len(args) != 1:
            print("формат: move <distance>")

        try:
            return cls(float(args[0]))
        except ValueError:
            print("distance должно быть числом")

# команда поворота
class TurnRobotCmd:
    name:  ClassVar[str] = "turn"

    def __init__(self, angle: float):
        self._angle = angle

    @property
    def angle(self) -> float:
        return self.angle

    def do(self, robot: Robot):
        robot.rotate(self._angle)
        print(f"ANGLE {degrees(robot.orientation):.2f}")

    @classmethod
    def from_args(cls, args: list[str]) -> Self:
        if len(args) != 1:
            print("формат: turn <angle>")
            return None
        try:
            angle = float(args[0])
            angle_rad = radians(angle)
            return cls(angle_rad)
        except ValueError:
            print("угол поворота нечисловой")

# команда установки тула
class SetToolRobotCmd:
    name: ClassVar[str] = "set"

    def __init__(self, tool: RobotTool):
        self._tool = tool

    def do(self, robot: Robot):
        robot._tool = self._tool
        print("STATE " + robot.tool)

    @classmethod
    def from_args(cls, args: list[str]) -> Self:
        if len(args) != 1:
            raise ValueError("формат: set <tool_name>")

        return cls(RobotTool(args[0]))

# команда старта с текущим тулом
class StartRobotCmd:
    name: ClassVar[str] = "start"

    def do(self, robot: Robot):
        print("START WITH " + robot.tool)

    @classmethod
    def from_args(cls, args: list[str]):
        if len(args) != 0:
            raise ValueError("формат: start")
        return cls()

# команда "стоп"
class StopRobotCmd:
    name: ClassVar[str] = "stop"

    def do(self, robot: Robot):
        print("STOP")

    @classmethod
    def from_args(cls, args: list[str]):
        if len(args) != 0:
            raise ValueError("формат: stop")
        return cls()

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


if __name__ == "__main__":
    # тестовый прогон из упражнения
    program = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]
    robot = Robot()
    interpreter = Interpreter(robot)
    interpreter.run(program)
    
    # неправильный синтаксис
    program = [
        "move 100",
        "turn -90",
        "set MAGIC SWORD", # ошибка
        "start",
        "move 50",
        "stop",
    ]
    robot2 = Robot()
    interpreter = Interpreter(robot2)
    interpreter.run(program)