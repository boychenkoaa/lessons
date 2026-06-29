import math
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Generic, Protocol, TypeVar

R = TypeVar("R")


class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


# -- классы ответов ---


class MoveResponse:
    def __init__(self, distance_moved: float, success: bool) -> None:
        self._distance_moved = distance_moved
        self._success = success

    @property
    def distance_moved(self) -> float:
        return self._distance_moved

    @property
    def success(self) -> bool:
        return self._success


class TurnResponse:
    def __init__(self, angle_turned: float, success: bool) -> None:
        self._angle_turned = angle_turned
        self._success = success

    @property
    def angle_turned(self) -> float:
        return self._angle_turned

    @property
    def success(self) -> bool:
        return self._success


class StateResponse:
    def __init__(self, mode: CleaningMode, success: bool) -> None:
        self._mode = mode
        self._success = success

    @property
    def mode(self) -> CleaningMode:
        return self._mode

    @property
    def success(self) -> bool:
        return self._success


# класс состояния робота теперь не мутирует


class RobotState:
    def __init__(self, x: float, y: float, angle: float, tool: int) -> None:
        self._x = x
        self._y = y
        self._angle = angle
        self._tool = tool

    @property
    def position(self) -> tuple[float, float]:
        return (self._x, self._y)

    @property
    def angle(self) -> float:
        return self._angle

    @property
    def tool(self) -> int:
        return self._tool

    # копирует с обновлениями указанных полей, типа x = 3.0
    def with_updates(self, **kwargs) -> "RobotState":
        current = {
            k.lstrip("_"): v for k, v in vars(self).items()
        }  # убирает у ключей префикс "_"
        current.update(kwargs)
        return RobotState(**current)

    def __repr__(self) -> str:
        return (
            f"RobotState(x={self._x:.2f}, y={self._y:.2f}, "
            f"angle={self._angle:.1f}, tool={self._tool})"
        )


# -- программа --
class RobotProgram(Protocol):
    def interpret(self, state: RobotState) -> tuple[Any, RobotState]: ...


# -- классы команд


class _Command(ABC):
    @abstractmethod
    def interpret(self, state: RobotState) -> tuple[Any, RobotState]: ...


class _Stop(_Command):
    def interpret(self, state: RobotState) -> tuple[None, RobotState]:
        return None, state

    def __repr__(self) -> str:
        return "Stop()"


class _RobotCmd(_Command, Generic[R]):
    def __init__(self, next_cmd: Callable[[R], RobotProgram]) -> None:
        self._next = next_cmd

    def interpret(self, state: RobotState) -> tuple[Any, RobotState]:
        new_state, response = self._do(state)
        return self._next(response), new_state

    @abstractmethod
    def _do(self, state: RobotState) -> tuple[RobotState, Any]: ...


class _Move(_RobotCmd[MoveResponse]):
    def __init__(
        self, distance: float, next_cmd: Callable[[MoveResponse], RobotProgram]
    ) -> None:
        self._distance = distance
        super().__init__(next_cmd)

    def _do(self, state: RobotState) -> tuple[RobotState, MoveResponse]:
        angle_rads = state._angle * (math.pi / 180.0)
        new_state = state.with_updates(
            x=state._x + self._distance * math.cos(angle_rads),
            y=state._y + self._distance * math.sin(angle_rads),
        )
        return new_state, MoveResponse(self._distance, True)


class _Turn(_RobotCmd[TurnResponse]):
    def __init__(
        self, angle: float, next_cmd: Callable[[TurnResponse], RobotProgram]
    ) -> None:
        self._angle = angle
        super().__init__(next_cmd)

    def _do(self, state: RobotState) -> tuple[RobotState, TurnResponse]:
        new_state = state.with_updates(angle=state._angle + self._angle)
        return new_state, TurnResponse(self._angle, True)


class _SetState(_RobotCmd[StateResponse]):
    def __init__(
        self, mode: CleaningMode, next_cmd: Callable[[StateResponse], RobotProgram]
    ) -> None:
        self._mode = mode
        super().__init__(next_cmd)

    def _do(self, state: RobotState) -> tuple[RobotState, StateResponse]:
        new_state = state.with_updates(tool=self._mode.value)
        return new_state, StateResponse(self._mode, True)


# -- фабричные функции --


def make_stop() -> RobotProgram:
    return _Stop()


def make_move(
    distance: float, next_cmd: Callable[[MoveResponse], RobotProgram]
) -> RobotProgram:
    return _Move(distance, next_cmd)


def make_turn(
    angle: float, next_cmd: Callable[[TurnResponse], RobotProgram]
) -> RobotProgram:
    return _Turn(angle, next_cmd)


def make_set_state(
    mode: CleaningMode, next_cmd: Callable[[StateResponse], RobotProgram]
) -> RobotProgram:
    return _SetState(mode, next_cmd)
