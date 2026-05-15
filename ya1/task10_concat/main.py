from robot_api import RobotApi
from robot_factory import simple_robot_fn


if __name__ == "__main__":
    robot = RobotApi()
    robot.setup(simple_robot_fn)
    postfix_str = "100 move -90 turn soap set start 50 move stop"
    robot_state = robot.make_concat(postfix_str)
    print(robot_state)
