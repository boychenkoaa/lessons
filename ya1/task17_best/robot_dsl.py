from typing import Callable

from robot_commands import (
    CleaningMode,
    RobotProgram,
    RobotState,
    make_move,
    make_set_state,
    make_stop,
    make_turn,
)


# --- DSL --
# убрал явное создание команд, теперь через фабрики
class RobotDSL:
    def __init__(self) -> None:
        self._commands: list[Callable] = []

    def move(self, distance: float) -> "RobotDSL":
        def create_move(next_cmd):
            return make_move(distance, next_cmd)

        self._commands.append(create_move)
        return self

    def turn(self, angle: float) -> "RobotDSL":
        def create_turn(next_cmd):
            return make_turn(angle, next_cmd)

        self._commands.append(create_turn)
        return self

    def set_mode(self, mode: CleaningMode) -> "RobotDSL":
        def create_set(next_cmd):
            return make_set_state(mode, next_cmd)

        self._commands.append(create_set)
        return self

    def build(self) -> RobotProgram:
        program = make_stop()
        for cmd_creator in reversed(self._commands):
            next_program = program
            program = cmd_creator(lambda r, next=next_program: next)
        return program

    def repeat(self, times: int, block: Callable[["RobotDSL"], None]) -> "RobotDSL":
        temp_dsl = RobotDSL()
        block(temp_dsl)
        block_commands = list(temp_dsl._commands)
        for _ in range(times):
            self._commands.extend(block_commands)
        return self

    def sequence(self, *commands: Callable[["RobotDSL"], None]) -> "RobotDSL":
        for cmd in commands:
            cmd(self)
        return self


# подпрограммы


def square(size: float) -> Callable[["RobotDSL"], None]:
    def program(dsl: RobotDSL) -> None:
        dsl.repeat(4, lambda r: r.move(size).turn(90))

    return program


def zigzag(length: float, count: int) -> Callable[["RobotDSL"], None]:
    def program(dsl: RobotDSL) -> None:
        dsl.repeat(count, lambda r: r.move(length).turn(45).move(length / 2).turn(-45))

    return program


# --- Интерпретатор --
# из цикла убрал проверку на инстанс стопа после переделки классов команд
class Interpreter:
    def run(self, program: RobotProgram, initial_state: RobotState) -> RobotState:
        current_program = program
        current_state = initial_state
        while current_program is not None:
            next_program, current_state = current_program.interpret(current_state)
            current_program = next_program
        return current_state
