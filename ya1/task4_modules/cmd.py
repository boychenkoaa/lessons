from math import radians, degrees
from typing import ClassVar, Self

from robot import Robot, RobotTool


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
