from typing import Callable, Tuple, TypeVar

import pure_robot as pr

# базовые типы

ValueT = TypeVar("ValueT")
TransferFn = Callable[[object], None]

ValueCapPair = Tuple[ValueT, "Capability"]
RobotMonad = Callable[["Capability"], ValueCapPair[ValueT]]
MonadFN = Callable[[ValueT], RobotMonad[ValueT]]


# функция - пустышка
# возвращаем ее когда требуемая функция недоступна


def unavailable(reason: str):
    def _raise(*args, **kwargs):
        raise RuntimeError(f"Недоступно: {reason}")

    return _raise


# собственно Capability c функциями
# возвращается вместо состояния


class Capability:
    _state: pr.RobotState
    _transfer: TransferFn

    move: Callable
    turn: Callable
    set_state: Callable
    start: Callable
    stop: Callable

    def __init__(self, state: pr.RobotState, builder: "CapabilityBuilder") -> None:
        self._state = state
        self._builder = builder

    def _move(self, dist: float) -> "Capability":
        new_state = pr.move(self._builder._transfer, dist, self._state)
        return self._builder.build(new_state)

    def _turn(self, angle: float) -> "Capability":
        new_state = pr.turn(self._builder._transfer, angle, self._state)
        return self._builder.build(new_state)

    def _set_state(self, mode: str) -> "Capability":
        new_state = pr.set_state(self._builder._transfer, mode, self._state)
        return self._builder.build(new_state)

    def _start(self) -> "Capability":
        new_state = pr.start(self._builder._transfer, self._state)
        return self._builder.build(new_state)

    def _stop(self) -> "Capability":
        new_state = pr.stop(self._builder._transfer, self._state)
        return self._builder.build(new_state)


# билдер для Capability
# доменные ограничения тоже держим в нем, при дальнейшем расширении надо выносить


class CapabilityBuilder:
    def __init__(
        self,
        transfer: TransferFn,
        bounds: tuple[float, float, float, float] | None = None,
    ) -> None:
        self._transfer = transfer
        self._bounds = bounds  # (x_min, x_max, y_min, y_max)

    def build(self, state: pr.RobotState) -> Capability:
        cap = Capability(state, self)
        ok = pr.can_move(state, self._bounds)
        cap.move = cap._move if ok else unavailable("мыльный пол")
        cap.turn = (
            cap._turn if pr.can_turn(state) else unavailable("поворот недоступен")
        )
        cap.set_state = (
            cap._set_state
            if pr.can_set_state(state)
            else unavailable("смена режима недоступна")
        )
        cap.start = (
            cap._start if pr.can_start(state) else unavailable("старт недоступен")
        )
        cap.stop = cap._stop if pr.can_stop(state) else unavailable("стоп недоступен")
        return cap


# монадные обертки


def move_cmd(dist: float) -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(cap: Capability) -> ValueCapPair[ValueT]:
            new_cap = cap.move(dist)
            return value, new_cap

        return run

    return make


def turn_cmd(angle: float) -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(cap: Capability) -> ValueCapPair[ValueT]:
            new_cap = cap.turn(angle)
            return value, new_cap

        return run

    return make


def set_state_cmd(mode: str) -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(cap: Capability) -> ValueCapPair[ValueT]:
            new_cap = cap.set_state(mode)
            return value, new_cap

        return run

    return make


def start_cmd() -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(cap: Capability) -> ValueCapPair[ValueT]:
            new_cap = cap.start()
            return value, new_cap

        return run

    return make


def stop_cmd() -> MonadFN[ValueT]:
    def make(value: ValueT) -> RobotMonad[ValueT]:
        def run(cap: Capability) -> ValueCapPair[ValueT]:
            new_cap = cap.stop()
            return value, new_cap

        return run

    return make


# "инфраструктура" монады


def init(value: ValueT) -> RobotMonad[ValueT]:
    def run(cap: "Capability") -> ValueCapPair[ValueT]:
        return value, cap

    return run


def bind(m: RobotMonad[ValueT], f: MonadFN[ValueT]) -> RobotMonad[ValueT]:
    def run(cap: "Capability") -> ValueCapPair[ValueT]:
        value, new_cap = m(cap)
        return f(value)(new_cap)

    return run


def pipe(initial: RobotMonad[ValueT], seq: list[MonadFN[ValueT]]) -> RobotMonad[ValueT]:
    ans = initial
    for f in seq:
        ans = bind(ans, f)
    return ans
