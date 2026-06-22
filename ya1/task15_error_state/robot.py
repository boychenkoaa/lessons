import math
from collections import namedtuple
from functools import wraps
from typing import Callable

# вкладываем в состояние робота
RobotState = namedtuple("RobotState", "x y angle state water_qty soap_qty")
RobotInfra = namedtuple("RobotInfra", "log ok", defaults=([], True))

WATER = 1
SOAP = 2
BRUSH = 3


class MoveResponse:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"


class SetStateResponse:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"


class IncWaterResponse:
    NEGATIVE = "NEGATIVE_WATER"


class StateMonad:
    def __init__(self, state, infra=None):
        self.state = state
        self.infra = infra or RobotInfra()

    def bind(self, func):
        if not self.infra.ok:
            return self
        new_state, new_infra = func(self.state, self.infra)
        return StateMonad(new_state, new_infra)

    def or_else(self, func):
        if self.infra.ok:
            return self
        new_state, new_infra = func(self.state, self.infra)
        return StateMonad(new_state, new_infra)


ROBOT_RECT = ((0, 0), (100, 100))

CheckStateFunc = Callable[[RobotState], bool]

# --- проверки ---


def robot_in_bounds(state: RobotState) -> bool:
    return (
        ROBOT_RECT[0][0] <= state.x <= ROBOT_RECT[1][0]
        and ROBOT_RECT[0][1] <= state.y <= ROBOT_RECT[1][1]
    )


def check_water(state: RobotState) -> bool:
    return state.water_qty > 0


def check_soap(state: RobotState) -> bool:
    return state.soap_qty > 0


def needs_water(mode: int, state: RobotState) -> bool:
    return mode != WATER or state.water_qty > 0


def needs_soap(mode: int, state: RobotState) -> bool:
    return mode != SOAP or state.soap_qty > 0


# --- декораторы ---
# декоратор - проверка предусловия с возвратом ошибки
def alarm_pre(check_func: CheckStateFunc, response):
    def wrapper(cmd_func):
        def inner(old_state, old_infra):
            if not check_func(old_state):
                return old_state, RobotInfra(
                    ok=False, log=old_infra.log + [f"ERROR: {response}"]
                )
            return cmd_func(old_state, old_infra)

        return inner

    return wrapper


# декоратор - проверка постуусловия с возвратом ошибки
def alarm_post(check_func: CheckStateFunc, response):
    def wrapper(cmd_func):
        def inner(old_state, old_infra):
            new_state, new_infra = cmd_func(old_state, old_infra)
            if not check_func(new_state):
                return new_state, RobotInfra(
                    ok=False, log=new_infra.log + [f"ERROR: {response}"]
                )
            return new_state, new_infra

        return inner

    return wrapper


# --- команды ---
def move(dist):
    @alarm_post(robot_in_bounds, MoveResponse.BARRIER)
    def inner(old_state: RobotState, old_infra: RobotInfra):
        angle_rads = old_state.angle * (math.pi / 180.0)
        new_state = RobotState(
            old_state.x + dist * math.cos(angle_rads),
            old_state.y + dist * math.sin(angle_rads),
            old_state.angle,
            old_state.state,
            old_state.water_qty,
            old_state.soap_qty,
        )
        new_infra = RobotInfra(
            log=old_infra.log + [f"POS({int(new_state.x)},{int(new_state.y)})"]
        )
        return new_state, new_infra

    return inner


def turn(angle):
    def inner(old_state: RobotState, old_infra: RobotInfra):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle + angle,
            old_state.state,
            old_state.water_qty,
            old_state.soap_qty,
        )
        new_infra = RobotInfra(log=old_infra.log + [f"ANGLE {new_state.angle}"])
        return new_state, new_infra

    return inner


def set_state(new_mode):
    @alarm_pre(lambda s: needs_water(new_mode, s), SetStateResponse.NO_WATER)
    @alarm_pre(lambda s: needs_soap(new_mode, s), SetStateResponse.NO_SOAP)
    def inner(old_state: RobotState, old_infra: RobotInfra):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle,
            new_mode,
            old_state.water_qty,
            old_state.soap_qty,
        )
        new_infra = RobotInfra(log=old_infra.log + [f"STATE {new_mode}"])
        return new_state, new_infra

    return inner


def start(old_state: RobotState, old_infra: RobotInfra):
    new_infra = RobotInfra(log=old_infra.log + ["START"])
    return old_state, new_infra


def stop(old_state: RobotState, old_infra: RobotInfra):
    new_infra = RobotInfra(log=old_infra.log + ["STOP"])
    return old_state, new_infra


def reset():
    def inner(old_state: RobotState, old_infra: RobotInfra):
        clean_state = RobotState(0, 0, 0, WATER, water_qty=100, soap_qty=50)
        new_infra = RobotInfra(log=old_infra.log + ["RESET"], ok=True)
        return clean_state, new_infra

    return inner


# добавил команду долива воды
# предусловие - количество после долива неотрицательно
def inc_water(amount):
    @alarm_pre(lambda s: s.water_qty + amount >= 0, IncWaterResponse.NEGATIVE)
    def inner(old_state: RobotState, old_infra: RobotInfra):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle,
            old_state.state,
            old_state.water_qty + amount,
            old_state.soap_qty,
        )
        new_infra = RobotInfra(log=old_infra.log + [f"WATER {amount:+}"])
        return new_state, new_infra

    return inner
