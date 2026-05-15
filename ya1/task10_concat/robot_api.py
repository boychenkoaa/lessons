from typing import Iterable

from pure_robot import WATER, RobotState
from robot_factory import RobotExecuteFn

class RobotApi:
    COMMANDS: tuple[str] = ("move", "turn", "set", "start", "stop")

    def setup(self, robot_fn: RobotExecuteFn) -> None:
        self._robot_fn = robot_fn
    
    def _is_command_name(self, lexem: str) -> bool:
        return lexem in self.COMMANDS
    
    def make_concat(self, postfix_str: str) -> RobotState:
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = RobotState(0.0, 0.0, 0, WATER)

        # используем стек
        lexems = postfix_str.split()
        args = ""
        for lexem in lexems:
            
            if self._is_command_name(lexem):
                command_str = lexem + ' ' + args
                self.cleaner_state = self._robot_fn([command_str], self.cleaner_state)     
                args = ""   
            else:
                args = lexem + " " + args
                
        return self.cleaner_state
