from math import atan2, degrees, hypot
from typing import NamedTuple
from base import RobotPose

class Rect(NamedTuple):
    x1: float
    y1: float
    x2: float
    y2: float

# генерирует программу движения в заданную позицию
def program_goto_pos(pose: RobotPose, target: RobotPose) -> list[str]:
    dx = target.x - pose.x
    dy = target.y - pose.y
    dist = hypot(dx, dy)
    if dist == 0:
        return [f"turn {target.angle - pose.angle}"]

    move_angle = degrees(atan2(dy, dx))
    turn_before = move_angle - pose.angle
    turn_after = target.angle - move_angle
    return [f"turn {turn_before}", f"move {dist}", f"turn {turn_after}"]

# генерирует программу обхода прямоугольника из текущего положения
def program_rect(width: float, height: float) -> list[str]:
    if width == 0 or height == 0:
        return []
    two_segments = [f"move {width}", "turn 90", f"move {height}", "turn 90"]
    return two_segments * 2

# генерирует программу обхода прямоугольника с заданными вершинами
def program_rect_abs(pose: RobotPose, rect: Rect) -> list[str]:
    width = abs(rect.x2 - rect.x1)
    height = abs(rect.y2 - rect.y1)
    
    left = min(rect.x1, rect.x2)
    bottom = min(rect.y1, rect.y2)
    start_pose = RobotPose(left, bottom, 0.0)
    ans = program_goto_pos(pose, start_pose)
    
    if width == 0 or height == 0:
        return ans

    ans.extend(program_rect(width, height))
    return ans

# генерирует программу заполнения прямоугольника, набором вложенных
def program_fill_rect(
    pose: RobotPose,
    rect: Rect,
    inset: float,
) -> list[str]:
    if inset <= 0:
        return []

    left = min(rect.x1, rect.x2)
    right = max(rect.x1, rect.x2)
    bottom = min(rect.y1, rect.y2)
    top = max(rect.y1, rect.y2)

    program: list[str] = []
    cur = pose

    while right - left > 0 and top - bottom > 0:
        segment = program_rect_abs(cur, Rect(left, bottom, right, top))
        program.extend(segment)

        cur = RobotPose(left, bottom, 0.0)

        left += inset
        right -= inset
        bottom += inset
        top -= inset

    return program

# генерирует программу очистки прямоугольника, 
# проходит набор вложенных прямоугольников
# сначала щеткой, потом шампунем, потом водой
def program_clean_rect(pose: RobotPose, rect: Rect, inset: float) -> list[str]:
    program: list[str] = []
    cur = pose
    left = min(rect.x1, rect.x2)
    bottom = min(rect.y1, rect.y2)
    start_pose = RobotPose(left, bottom, 0)
    
    for tool in ("brush", "soap", "water"):
        segment = program_fill_rect(cur, rect, inset)
        program.append(f"set {tool}")
        program.append("start")
        program.extend(segment)
        program.append("stop")

        # Возврат в левый нижний угол
        cur = start_pose

    return program
