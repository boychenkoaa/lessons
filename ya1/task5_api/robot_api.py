from math import atan2, degrees, hypot
from typing import NamedTuple

import pure_robot as pr
import programs as pg


# сессия работы с роботом -- подключена ли + состояние робота
class Session(NamedTuple):
    connected: bool
    robot: pr.RobotState

# базовые команды работы с сессией
def connect(robot: pr.RobotState) -> Session:
    return Session(True, robot)

def disconnect(robot: pr.RobotState) -> Session:
    return Session(False, robot)

# вспомогательная функция для краткости, чтобы не прописывать постоянно s.connected
def _with_robot(s: Session, robot: pr.RobotState) -> Session:
    return Session(s.connected, robot)

# исполнение кастомной программы
def run_program(s: Session, program: list[str]) -> Session:
    if not s.connected:
        print("Сессия не подключена")
        return s
    new_robot = pr.make(pr.transfer_to_cleaner, program, s.robot)
    return _with_robot(s, new_robot)

# очистка квадрата
# простой проброс параметров в run_program -- главное, что программа для робота написана
def clean_rect(
    s: Session, x1: float, y1: float, x2: float, y2: float, inset: float
) -> Session:
    pos = pg.Pos(s.robot.x, s.robot.y, s.robot.angle)
    rect = pg.Rect(x1, y1, x2, y2)
    program = pg.program_clean_rect(pos, rect, inset)
    return run_program(s, program)






    



