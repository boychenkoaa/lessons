from programs import Rect
from robot_api import build_cleaner_client

if __name__ == "__main__":
    # прогон простой программы 
    program = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]
    client = build_cleaner_client()
    client.run_program(program)

    # и "высокоуровневый" метод
    client.clean_rect(Rect(0.0, 0.0, 6.0, 4.0), 1.0)
