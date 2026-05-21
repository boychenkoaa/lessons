from pure_robot import RobotState, WATER, transfer_to_cleaner
from robot_api import compose, fold, move_cmd, turn_cmd, set_state_cmd

def main():
    initial_state = RobotState(0.0, 0.0, 0.0, WATER)

    commands_seq = [move_cmd(50), turn_cmd(90), set_state_cmd("soap"), move_cmd(5)]
    program = compose(cmd_sequence=commands_seq)
    final1 = program(initial_state)
    final2 = fold(initial_state, commands_seq)
    print(f"final1 = {final1}")
    print(f"final2 = {final2}")


if __name__ == "__main__":
    main()


