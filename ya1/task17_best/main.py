"""
Smoke-тест:
1. Прямое построение программы через фабрики
2. DSL: fluent-интерфейс + подпрограммы
"""

from robot_commands import (
    CleaningMode,
    RobotState,
    make_move,
    make_set_state,
    make_stop,
    make_turn,
)
from robot_dsl import Interpreter, RobotDSL, square, zigzag


def main() -> None:
    interpreter = Interpreter()
    initial_state = RobotState(x=0.0, y=0.0, angle=0.0, tool=CleaningMode.WATER.value)

    # генерим напрямую через фабрики
    program = make_move(
        100.0,
        lambda r: make_turn(
            -90.0,
            lambda r: make_set_state(
                CleaningMode.SOAP, lambda r: make_move(50.0, lambda r: make_stop())
            ),
        ),
    )

    initial = initial_state.with_updates()  # иммутабельная копия без изменений
    final = interpreter.run(program, initial)
    print(f"\nФабрики\n{initial}\n{final}")

    assert final.position == (100.0, -50.0)

    # создаем более синтаксически чисто через DSL
    dsl_program = (
        RobotDSL().move(100).turn(-90).set_mode(CleaningMode.SOAP).move(50).build()
    )

    initial = initial_state.with_updates()
    final = interpreter.run(dsl_program, initial)
    print(f"\nDSL\n{initial}\n{final}")


if __name__ == "__main__":
    main()
