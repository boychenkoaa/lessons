from pure_robot import RobotState
from robot_api_fp import DEFAULT_ROBOT, DEFAULT_INITIAL_STATE


if __name__ == "__main__":
    
    code = [
        "set water",
        "move 10",
        "turn 90",
        "start",
        "move 20",
        "stop",
    ]
    final_state = DEFAULT_ROBOT(code, DEFAULT_INITIAL_STATE)
    print(final_state)
