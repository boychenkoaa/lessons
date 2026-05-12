from abc import ABC, abstractmethod
from enum import StrEnum
from math import pi, sin, cos
from base import RobotPose

class RobotTool(StrEnum):
    SOAP = "soap"
    WATER = "water"
    BRUSH = "brush"

Point = tuple[float, float]
Orientation = float


class Robot(ABC):
    @abstractmethod
    def rotate(self, angle_rad: float):
        raise NotImplementedError

    @abstractmethod
    def move(self, dist: float):
        raise NotImplementedError

    @abstractmethod
    def set_tool(self, tool: RobotTool):
        raise NotImplementedError

    @property
    @abstractmethod
    def pos(self) -> Point:
        raise NotImplementedError

    @property
    @abstractmethod
    def pose(self) -> RobotPose:
        raise NotImplementedError

    @property
    @abstractmethod
    def tool(self) -> RobotTool:
        raise NotImplementedError

    @property
    @abstractmethod
    def orientation(self) -> Orientation:
        raise NotImplementedError


# класс робота 
# базовые действия робота + его состояние (позиция, ориентация, тул)

class Cleaner(Robot):
    def __init__(self):
        self._x = 0.0
        self._y = 0.0
        self._orientation = 0.0
        self._tool = RobotTool.WATER

    def rotate(self, angle_rad: float):
        self._orientation = (self._orientation + angle_rad) % (2 * pi)

    def move(self, dist: float):
        dx = dist * cos(self._orientation)
        dy = dist * sin(self._orientation)
        self._x += dx
        self._y += dy

    def set_tool(self, tool: RobotTool):
        self._tool = tool

    @property
    def pos(self) -> Point:
        return self._x, self._y
    
    @property
    def pose(self) -> RobotPose:
        return RobotPose(self._x, self._y, self._orientation)

    @property
    def tool(self) -> RobotTool:
        return self._tool

    @property
    def orientation(self) -> Orientation:
        return self._orientation
