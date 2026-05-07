from enum import StrEnum
from math import pi, sin, cos


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
