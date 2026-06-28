"""AST-based robot control — immutable architecture."""

import math
from collections import namedtuple
from enum import Enum
from typing import Any, Callable

WATER = 1
SOAP = 2
BRUSH = 3


# ответы
class MoveResponse(str, Enum):
    OK = "OK"
    NO_WATER = "NO_WATER"
    NO_SOAP = "NO_SOAP"


class TurnResponse(str, Enum):
    OK = "OK"


class StateResponse(str, Enum):
    OK = "OK"
    NO_WATER = "NO_WATER"
    NO_SOAP = "NO_SOAP"


# контекст = состояние робота + состояние инфраструктуры
RobotState = namedtuple("RobotState", "x y angle state water_qty soap_qty")
RobotInfra = namedtuple("RobotInfra", "log response")
RobotContext = namedtuple("RobotContext", "state infra")


# классы команд
class Cmd:
    # абстрактная команда, она же -- нода дерева.
    # do переопределяется в потомках
    # interpret - общий

    def __init__(self, next: Callable[["RobotContext"], "Cmd"] | None = None):
        self._next = next

    # тут доменная логика - что делает робот
    def do(self, state: RobotState) -> tuple[RobotState, str]:
        raise NotImplementedError

    # оберка для доменной логики
    # ответы команд пишем в логи
    # рекурсивно вызываем следующую
    def interpret(self, ctx: RobotContext) -> RobotContext:
        new_state, response = self.do(ctx.state)
        new_infra = RobotInfra(
            log=ctx.infra.log + (response,),
            response=response,
        )
        new_ctx = RobotContext(state=new_state, infra=new_infra)
        if self._next is None:
            return new_ctx
        return self._next(new_ctx).interpret(new_ctx)


class Stop(Cmd):
    # в команде СТОП -- next игнорируется

    def interpret(self, ctx: RobotContext) -> RobotContext:
        return ctx._replace(infra=RobotInfra(log=ctx.infra.log, response="STOP"))


class Move(Cmd):
    def __init__(self, distance: int, next: Callable[["RobotContext"], "Cmd"]):
        super().__init__(next)
        self.distance = distance

    # добавил проверку, может ли робот идти  с учетом расхода
    # расход 1  единица на единицу длины
    def do(self, state: RobotState) -> tuple[RobotState, MoveResponse]:
        rad = math.radians(state.angle)
        x = state.x + self.distance * math.cos(rad)
        y = state.y + self.distance * math.sin(rad)

        water = state.water_qty
        soap = state.soap_qty

        if state.state == WATER:
            if water >= self.distance:
                water -= self.distance
            else:
                return state, MoveResponse.NO_WATER
        elif state.state == SOAP:
            if soap >= self.distance:
                soap -= self.distance
            else:
                return state, MoveResponse.NO_SOAP

        new_state = state._replace(x=x, y=y, water_qty=water, soap_qty=soap)
        return new_state, MoveResponse.OK


class Turn(Cmd):
    def __init__(self, angle: int, next: Callable[["RobotContext"], "Cmd"]):
        super().__init__(next)
        self.angle = angle

    def do(self, state: RobotState) -> tuple[RobotState, TurnResponse]:
        new_angle = (state.angle + self.angle) % 360
        new_state = state._replace(angle=new_angle)
        return new_state, TurnResponse.OK


class SetState(Cmd):
    def __init__(self, mode: int, next: Callable[["RobotContext"], "Cmd"]):
        super().__init__(next)
        self.mode = mode

    def do(self, state: RobotState) -> tuple[RobotState, StateResponse]:
        if self.mode == WATER and state.water_qty <= 0:
            return state, StateResponse.NO_WATER
        if self.mode == SOAP and state.soap_qty <= 0:
            return state, StateResponse.NO_SOAP
        new_state = state._replace(state=self.mode)
        return new_state, StateResponse.OK


# обертка инфраструктурная, для демонстрации
# если закончилась пена -- можем переключиться на воду (сложный вариант)
# простой вариант -- остановиться, его можно и через лямбду
def switch2water_and_move(
    ctx: RobotContext, nxt: Callable[[RobotContext], Cmd], distance: int = 0
) -> Cmd:
    match ctx.infra.response:
        case MoveResponse.OK:
            return nxt(ctx)
        case MoveResponse.NO_WATER:
            return Stop()
        case MoveResponse.NO_SOAP:
            return SetState(WATER, next=lambda ctx: Move(distance, next=nxt))
        case _:
            return Stop()
