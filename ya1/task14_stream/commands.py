from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Protocol

from base import CleaningMode, RobotState
from events import (
    Event,
    RobotMovedRequestEvent,
    RobotResetRequestEvent,
    RobotStartedRequestEvent,
    RobotStateChangedRequestEvent,
    RobotStoppedRequestEvent,
    RobotTurnedRequestEvent,
)


class Command(Protocol):
    @abstractmethod
    def handle(self, robot_id: str, current_state: RobotState) -> List[Event]:
        pass

    def get_command_type(self) -> str:
        return "ABC Command"


@dataclass
class MoveCommand:
    distance: float

    def handle(self, robot_id: str, current_state: RobotState) -> List[Event]:
        return [RobotMovedRequestEvent(robot_id, self.distance)]

    def get_command_type(self) -> str:
        return f"MOVE {self.distance}"


@dataclass
class TurnCommand:
    angle: float

    def handle(self, robot_id: str, current_state: RobotState) -> List[Event]:
        return [RobotTurnedRequestEvent(robot_id, self.angle)]

    def get_command_type(self) -> str:
        return f"TURN {self.angle}"


@dataclass
class SetStateCommand:
    new_state: CleaningMode

    def handle(self, robot_id: str, current_state: RobotState) -> List[Event]:
        return [RobotStateChangedRequestEvent(robot_id, self.new_state)]

    def get_command_type(self) -> str:
        return f"SET_STATE {self.new_state.name}"


@dataclass
class StartCommand:
    def handle(self, robot_id: str, current_state: RobotState) -> List[Event]:
        return [RobotStartedRequestEvent(robot_id)]

    def get_command_type(self) -> str:
        return "START"


@dataclass
class StopCommand:
    def handle(self, robot_id: str, current_state: RobotState) -> List[Event]:
        return [RobotStoppedRequestEvent(robot_id)]

    def get_command_type(self) -> str:
        return "STOP"


@dataclass
class ResetCommand:
    def handle(self, robot_id: str, current_state: RobotState) -> List[Event]:
        return [RobotResetRequestEvent(robot_id)]

    def get_command_type(self) -> str:
        return "RESET"


class CommandHandler:
    def handle_command(
        self,
        robot_id: str,
        command: Command,
        current_state: RobotState,
    ) -> List[Event]:
        return command.handle(robot_id, current_state)
