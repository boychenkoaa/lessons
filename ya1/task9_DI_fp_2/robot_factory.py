from typing import Callable, Iterable

from pure_robot import (
    WATER,
    RobotState,
    move,
    set_state,
    start,
    stop,
    transfer_to_cleaner,
    turn,
)

TransferFn = Callable
MoveFn = Callable[[TransferFn, float, RobotState], RobotState]
TurnFn = Callable[[TransferFn, float, RobotState], RobotState]
SetStateFn = Callable[[TransferFn, str, RobotState], RobotState]
StartFn = Callable[[TransferFn, RobotState], RobotState]
StopFn = Callable[[TransferFn, RobotState], RobotState]
RobotExecuteFn = Callable[[Iterable[str], RobotState], RobotState]

"""
make_robot по сути, фабрика роботв, только функциональная
принимает на вход функции движения робота -- 5 шт.
Возвращает конкретную функцию-исполнителя, которая выполняет код.

Это оправдано, так как юзер вряд ли будет бесконечно комбинировать эти функции.
Сужается степень свободы для юзера, расширяется набор предподготовленных роботов и упрощается контракт API
"""

DEFAULT_INITIAL_STATE = RobotState(0, 0, 0, WATER)

def double_move(transfer,dist,state):
    return move(transfer, dist * 2, state)

def make_robot(
    move_fn: MoveFn,
    turn_fn: TurnFn,
    set_state_fn: SetStateFn,
    start_fn: StartFn,
    stop_fn: StopFn,
    transfer_fn: TransferFn
) -> RobotExecuteFn:
    def execute(code: Iterable[str], state: RobotState) -> RobotState:
        for command in code:
            cmd = command.split()
            if cmd[0] == "move":
                state = move_fn(transfer_fn, float(cmd[1]), state)
            elif cmd[0] == "turn":
                state = turn_fn(transfer_fn, float(cmd[1]), state)
            elif cmd[0] == "set":
                state = set_state_fn(transfer_fn, cmd[1], state)
            elif cmd[0] == "start":
                state = start_fn(transfer_fn, state)
            elif cmd[0] == "stop":
                state = stop_fn(transfer_fn, state)
        return state

    return execute

# эти функции-роботы как раз и делаются фабрикой
# передаем их в API

simple_robot_fn = make_robot(
        move_fn=move,
        turn_fn=turn,
        set_state_fn=set_state,
        start_fn=start,
        stop_fn=stop,
        transfer_fn=transfer_to_cleaner,
    )


fast_robot_fn = make_robot(
        move_fn=double_move,
        turn_fn=turn,
        set_state_fn=set_state,
        start_fn=start,
        stop_fn=stop,
        transfer_fn=transfer_to_cleaner,
    )
