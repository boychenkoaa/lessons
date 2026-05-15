from typing import Iterable

from pure_robot import WATER, RobotState
from robot_factory import RobotExecuteFn

class RobotApi:
    def setup(self, robot_fn: RobotExecuteFn):
        self._robot_fn = robot_fn
        

    def make(self, code: Iterable[str]) -> RobotState:
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = RobotState(0.0, 0.0, 0, WATER)

        self.cleaner_state = self._robot_fn(code, self.cleaner_state)
        return self.cleaner_state

    def __call__(self, code: Iterable[str]) -> RobotState:
        return self.make(code)
