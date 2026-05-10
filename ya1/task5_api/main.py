import pure_robot as pr
from robot_api import connect, clean_rect


if __name__ == "__main__":
    initial = pr.RobotState(0.0, 0.0, 0.0, pr.WATER)
    session = connect(initial)
    session = clean_rect(session, 0.0, 0.0, 6.0, 4.0, 1.0)
    print("Final state:", session.robot)
