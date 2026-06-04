from pure_robot import WATER, SOAP, BRUSH, RobotState
from robot_commands import move_cmd, turn_cmd
from command_handler import EventStore, CommandHandler  

def main():
    event_store = EventStore()
    initial_state = RobotState(0.0, 0.0, 0.0, WATER)
    print(f"initial = {initial_state}")
    cmd_handler = CommandHandler(event_store, initial_state)
    state1 = cmd_handler.run(move_cmd(50))
    state2 = cmd_handler.run(turn_cmd(90))
    state3 = cmd_handler.run(move_cmd(40))
    state4 = cmd_handler.run(turn_cmd(90))
    state5 = cmd_handler.run(move_cmd(30))
    state6 = cmd_handler.undo()
    state7 = cmd_handler.undo()
    state8 = cmd_handler.redo()
    state9 = cmd_handler.redo()
    assert (state3 == state7)
    assert (state4 == state6)
    assert (state4 == state8)
    assert (state5 == state9)
    print("===\nOK")
    
if __name__ == "__main__":
    main()
