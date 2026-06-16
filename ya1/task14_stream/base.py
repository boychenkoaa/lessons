from dataclasses import dataclass
from enum import Enum


@dataclass
class RobotState:
    x: float
    y: float
    angle: float
    state: int
    is_error: bool = False
    error_message: str = ""

    def __repr__(self) -> str:
        base = (
            f"RobotState(x={self.x:.1f}, y={self.y:.1f}, "
            f"angle={self.angle:.1f}, {CleaningMode(self.state).name}"
        )
        if self.is_error:
            return base + f", error={self.error_message!r})"
        return base + ")"


class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


def clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))
