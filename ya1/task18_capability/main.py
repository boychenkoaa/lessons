from pure_robot import WATER, RobotState, transfer_to_cleaner
from robot_api import (
    CapabilityBuilder,
    init,
    move_cmd,
    pipe,
    set_state_cmd,
    start_cmd,
    stop_cmd,
    turn_cmd,
)


def main() -> None:
    initial_state = RobotState(0.0, 0.0, 0.0, WATER)
    builder = CapabilityBuilder(transfer_to_cleaner)
    initial_cap = builder.build(initial_state)

    print("--- Попытка move на мыльном полу ---")
    program2 = pipe(
        init(None),
        [
            start_cmd(),
            move_cmd(100.0),
            turn_cmd(-90.0),
            set_state_cmd("soap"),
            move_cmd(50.0),  # ошибка
            stop_cmd(),
        ],
    )
    try:
        _, cap2 = program2(initial_cap)
    except RuntimeError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
