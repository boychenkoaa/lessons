from typing import Callable, TypeVar, Tuple
from pure_robot import RobotState, move, turn, start, stop, set_state

# аннотации

ValueT = TypeVar("ValueT")

TransferFn = Callable[[object], None]

ValueStatePair = Tuple[ValueT, RobotState]
RobotMonad = Callable[[RobotState], ValueStatePair[ValueT]]
MonadFN = Callable[[ValueT], RobotMonad[ValueT]]


# "монадные" обертки функций pure_robot


def move_cmd(transfer: TransferFn, dist: float) -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(state: RobotState) -> ValueStatePair[ValueT]:
            new_state = move(transfer, dist, state)
            return value, new_state

        return run

    return make


def turn_cmd(transfer: TransferFn, angle: float) -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(state: RobotState) -> ValueStatePair[ValueT]:
            new_state = turn(transfer, angle, state)
            return value, new_state

        return run

    return make


def set_state_cmd(transfer: TransferFn, new_internal_state: str) -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(state: RobotState) -> ValueStatePair[ValueT]:
            new_state = set_state(transfer, new_internal_state, state)
            return value, new_state

        return run

    return make


def start_cmd(transfer: TransferFn) -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(state: RobotState) -> ValueStatePair[ValueT]:
            new_state = start(transfer, state)
            return value, new_state

        return run

    return make


def stop_cmd(transfer: TransferFn) -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(state: RobotState) -> ValueStatePair[ValueT]:
            new_state = stop(transfer, state)
            return value, new_state

        return run

    return make


# API

# это класс без состояния, ну разве что transfer_to_cleaner хранится
# нужен, в общем-то, только для каррирования


class RobotApi:
    def __init__(self, transfer_fn: TransferFn):
        self._transfer_fn = transfer_fn

    def move(self, dist: float) -> MonadFN[ValueT]:
        return move_cmd(self._transfer_fn, dist)

    def turn(self, angle: float) -> MonadFN[ValueT]:
        return turn_cmd(self._transfer_fn, angle)

    def set_state(self, new_internal_state: str) -> MonadFN[ValueT]:
        return set_state_cmd(self._transfer_fn, new_internal_state)

    def start(self) -> MonadFN[ValueT]:
        return start_cmd(self._transfer_fn)

    def stop(self) -> MonadFN[ValueT]:
        return stop_cmd(self._transfer_fn)


def make_api(transfer_fn: TransferFn) -> RobotApi:
    return RobotApi(transfer_fn)


# собственно bind / init / pipe - мета-функции, если так можно выразиться
# функции более высокого порядка (?)


def bind(m: RobotMonad[ValueT], f: MonadFN[ValueT]) -> RobotMonad[ValueT]:
    def run(state: RobotState) -> ValueStatePair[ValueT]:
        value, new_state = m(state)
        return f(value)(new_state)

    return run


def init(value: ValueT) -> RobotMonad[ValueT]:
    def run(state: RobotState) -> ValueStatePair[ValueT]:
        return value, state

    return run


def pipe(initial: RobotMonad[ValueT], functions_seq: list[MonadFN[ValueT]]) -> RobotMonad[ValueT]:
    ans = initial
    for f in functions_seq:
        ans = bind(ans, f)
    return ans
