import pure_robot as pr
from robot_api import clean_rect, close_session, create_session


if __name__ == "__main__":
    session = create_session()
    session = clean_rect(session, 0.0, 0.0, 6.0, 4.0, 1.0)
    session = close_session()
    print("Final state:", session.robot)
