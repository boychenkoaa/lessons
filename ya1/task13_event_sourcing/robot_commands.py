from functools import reduce
from typing import Callable, Sequence

from pure_robot import move, turn, set_state, start, stop, RobotState, transfer_to_cleaner

Cmd = Callable[[RobotState], RobotState]

# команды-функции-обертки, возвращают замыкание
def move_cmd(dist: float) -> Cmd:
    def run(state: RobotState) -> RobotState:
        return move(transfer_to_cleaner, dist, state)

    return run


def turn_cmd(angle: float) -> Cmd:
    def run(state: RobotState) -> RobotState:
        return turn(transfer_to_cleaner, angle, state)

    return run


def set_state_cmd(new_internal_state: str) -> Cmd:
    def run(state: RobotState) -> RobotState:
        return set_state(transfer_to_cleaner, new_internal_state, state)

    return run


def start_cmd() -> Cmd:
    def run(state: RobotState) -> RobotState:
        return start(transfer_to_cleaner, state)

    return run


def stop_cmd() -> Cmd:
    def run(state: RobotState) -> RobotState:
        return stop(transfer_to_cleaner, state)

    return run

# команды следующего уровня -- композиция и свертка
def fold(initial: RobotState, cmd_sequence: Sequence[Cmd]) -> RobotState:
    return reduce(lambda state, cmd: cmd(state), cmd_sequence, initial)


def compose(cmd_sequence: Sequence[Cmd]) -> Cmd:
    def run(state: RobotState) -> RobotState:
        return reduce(lambda state, cmd: cmd(state), cmd_sequence, state)

    return run