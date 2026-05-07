"""
Рефлексия по предыдущему решению:

Мое изначальное решение было в стиле ООП.

Фундаментальные ограничения: 
- отсутствует полноценный парсер и лексический анализатор
- не поддерживается внутреннее состояние программы

Можно добавить:
- несколько строк => одна команда
- вложенные команды без состояния (повторить N раз, повторять пока не будет нажат пробел...)

Преодолеваемые ограничения (не уверен, но можно попробовать)
- добавить ветвления и GOTO (но без глобальных переменных -- зачем?)

Расширяемость:
набор команд можно без особенных сложностей расширить на порядок
да, будет 50 классов команд и огромный словарь, но само расширение делается достаточно прозрачно
"""

"""
Комментарий к текущему решению в структурном стиле
Я постараюсь пользоваться только теми возможностями языка, которые были у Дейкстры (их аналогами в Python)
За основу возьму Алгол-68
- там были структуры -- значит я могу использовать датаклассы :)
- наследовать нельзя, вкладывать можно
- нет ассоциативных массивов, но есть обычные массивы и указатели на функции

UPD: некоторый синтаксический сахар я все же использовал, но общей архитектуры он не поменял
Структуры команд вырожденными получились, из одного поля или вообще пустые.
Возможно, переусложнил.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from math import pi, sin, cos, radians, degrees
from typing import Callable

class RobotTool(StrEnum):
    SOAP = "soap"
    WATER = "water"
    BRUSH = "brush"
    
ALLOWED_TOOLS = "|".join(tool.value for tool in RobotTool)

@dataclass
class RobotPos:
    x: float = 0.0
    y: float = 0.0
    
@dataclass
class MoveCmd:
    distance: float = 0.0


@dataclass
class TurnCmd:
    angle: float = 0.0


@dataclass
class SetToolCmd:
    tool: RobotTool = RobotTool.WATER


@dataclass
class StartCmd:
    pass


@dataclass
class StopCmd:
    pass


@dataclass
class Robot:
    pos: RobotPos = field(default_factory=RobotPos)
    orientation: float = 0.0
    tool: RobotTool = RobotTool.WATER

def move_pos(pos: RobotPos, dx: float, dy: float) -> RobotPos:
    return RobotPos(pos.x + dx, pos.y + dy)    
    
def move_robot(robot: Robot, dist: float):
    dx = dist * cos(robot.orientation)
    dy = dist * sin(robot.orientation)
    robot.pos = move_pos(robot.pos, dx, dy)


def turn_robot(robot: Robot, angle: float):
    robot.orientation = (robot.orientation + angle) % (2 * pi)


def create_move(args: list[str]) -> MoveCmd:
    if len(args) != 1:
        raise ValueError("формат: move <distance>")
    try:
        return MoveCmd(float(args[0]))
    except ValueError:
        print(f"\nERROR: distance: ожидалось число, введено {args[0]}")


def exec_move(robot: Robot, cmd: MoveCmd):
    move_robot(robot, cmd.distance)
    print(f"POS {robot.pos.x:.2f}, {robot.pos.y:.2f}")


def create_turn(args: list[str]) -> TurnCmd:
    if len(args) != 1:
        raise ValueError("формат: turn <angle_degrees>")
    try:
        return TurnCmd(radians(float(args[0])))
    except ValueError:
        print(f"\nERROR: angle: ожидалось число, введено {args[0]}")


def exec_turn(robot: Robot, cmd: TurnCmd):
    turn_robot(robot, cmd.angle)
    print(f"ANGLE {degrees(robot.orientation):.2f}")


def create_set(args: list[str]) -> SetToolCmd:
    
    if len(args) != 1:
        print(f"\nERROR: формат должен быть: set <{ALLOWED_TOOLS}>")
        return None
    
    try:
        ans = SetToolCmd(RobotTool(args[0]))
    except ValueError:
        print(f"\nERROR: Tool: ожидалось значение из {ALLOWED_TOOLS}, получено {args[0]}")
        ans = None
    return ans


def exec_set(robot: Robot, cmd: SetToolCmd):
    robot.tool = cmd.tool
    print(f"STATE {robot.tool}")


def create_start(args: list[str]) -> StartCmd:
    if len(args) != 0:
        print("\nERROR: формат команды должен быть \'start\'")
        return None
    return StartCmd()


def exec_start(robot: Robot, cmd: StartCmd):
    print("START WITH " + robot.tool)


def create_stop(args: list[str]) -> StopCmd:
    if len(args) != 0:
        print("\nERROR: формат: start")
        return None
    return StopCmd()


def exec_stop(robot: Robot, cmd: StopCmd):
    print("STOP")


COMMAND_NAMES = ("move", "turn", "set", "start", "stop")
COMMAND_CREATORS = (
    create_move,
    create_turn,
    create_set,
    create_start,
    create_stop,
)
COMMAND_EXECUTORS = (
    exec_move,
    exec_turn,
    exec_set,
    exec_start,
    exec_stop,
)


def find_command_index(command_name: str) -> int:
    for i in range(len(COMMAND_NAMES)):
        if COMMAND_NAMES[i] == command_name:
            return i
    return -1

def interpret_line(line: str, robot: Robot):
    line_parts = line.split()
    if len(line_parts) == 0:
        return
    cmd_name = line_parts[0]
    args = line_parts[1:]

    cmd_index = find_command_index(cmd_name)
    if cmd_index < 0:
        print(f"\nERROR: Неизвестная команда: {cmd_name}")
        return

    creator = COMMAND_CREATORS[cmd_index]
    executor = COMMAND_EXECUTORS[cmd_index]

    try:
        cmd = creator(args)
        executor(robot, cmd)
    except:
        print(f"\nERROR: ошибка в строке '{line}'\n")


def interpret_program(program: list[str], robot: Robot):
    for line in program:
        interpret_line(line, robot)


if __name__ == "__main__":
    # Тестовый прогон из упражнения
    program = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]
    robot = Robot()
    interpret_program(program, robot)

    # Прогон с ошибкой формата/аргументов
    bad_program = [
        "move 100",
        "turn -90",
        "set MAGIC_SWORD",
        "start",
        "move 50",
        "stop",
    ]
    robot2 = Robot()
    interpret_program(bad_program, robot2)
