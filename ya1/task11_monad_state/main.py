from pure_robot import RobotState, WATER, transfer_to_cleaner
from robot_api import (
    make_api,
    init,
    pipe,
)


def main() -> None:
    initial_state = RobotState(0.0, 0.0, 0.0, WATER)
    api = make_api(transfer_to_cleaner)

    program = pipe(
        init(None),
        [
            api.start(),
            api.move(100.0),
            api.turn(-90.0),
            api.set_state("soap"),
            api.move(50.0),
            api.stop(),
        ],
    )

    _, final_state = program(initial_state)
    print("FINAL:", final_state)


if __name__ == "__main__":
    main()


