from typing import NamedTuple

# поза - позиция + ориентация
class RobotPose(NamedTuple):
    x: float
    y: float
    angle: float
