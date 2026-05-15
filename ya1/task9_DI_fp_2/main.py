from robot_api import RobotApi
from robot_factory import fast_robot_fn, simple_robot_fn


if __name__ == "__main__":
    code = [
        "set water",
        "move 10",
        "turn 90",
        "move 5",
    ]

    robot = RobotApi()
    robot.setup(simple_robot_fn)
    robot_state = robot(code)
    print(f"simple: {robot_state}")

    robot.setup(fast_robot_fn)
    robot_state = robot(code)
    print(f"fast: {robot_state}")
