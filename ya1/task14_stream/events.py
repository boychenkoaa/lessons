import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, List, TypeVar, cast

from base import CleaningMode, RobotState

TEvent = TypeVar("TEvent", bound="Event")
TRequestEvent = TypeVar("TRequestEvent", bound="RequestEvent")
TResultEvent = TypeVar("TResultEvent", bound="ResultEvent")


class Event(ABC):
    robot_id: str

    @abstractmethod
    def get_event_type(self) -> str:
        pass


class RequestEvent(Event):
    def get_event_type(self) -> str:
        return "Request"


@dataclass
class RobotMovedRequestEvent(RequestEvent):
    robot_id: str
    distance: float

    def get_event_type(self) -> str:
        return f"{super().get_event_type()} | ROBOT_MOVED {self.distance}"


@dataclass
class RobotTurnedRequestEvent(RequestEvent):
    robot_id: str
    angle: float

    def get_event_type(self) -> str:
        return f"{super().get_event_type()} | ROBOT_TURNED {self.angle}"


@dataclass
class RobotStateChangedRequestEvent(RequestEvent):
    robot_id: str
    new_state: CleaningMode

    def get_event_type(self) -> str:
        return f"{super().get_event_type()} | ROBOT_STATE_CHANGED {self.new_state.name}"


@dataclass
class RobotStartedRequestEvent(RequestEvent):
    robot_id: str

    def get_event_type(self) -> str:
        return f"{super().get_event_type()} | ROBOT_STARTED"


@dataclass
class RobotStoppedRequestEvent(RequestEvent):
    robot_id: str

    def get_event_type(self) -> str:
        return f"{super().get_event_type()} | ROBOT_STOPPED"


@dataclass
class RobotResetRequestEvent(RequestEvent):
    robot_id: str

    def get_event_type(self) -> str:
        return f"{super().get_event_type()} | ROBOT_RESET"


class ResultEvent(Event):
    def apply(self, state: RobotState, applier: "ResultEventApplier") -> RobotState:
        return applier.apply_noop(self, state)


@dataclass
class RobotMovedResultEvent(ResultEvent):
    robot_id: str
    distance: float

    def apply(self, state: RobotState, applier: "ResultEventApplier") -> RobotState:
        return applier.apply_moved(self, state)

    def get_event_type(self) -> str:
        return f"ROBOT_MOVED {self.distance}"


@dataclass
class RobotTurnedResultEvent(ResultEvent):
    robot_id: str
    angle: float

    def apply(self, state: RobotState, applier: "ResultEventApplier") -> RobotState:
        return applier.apply_turned(self, state)

    def get_event_type(self) -> str:
        return f"ROBOT_TURNED {self.angle}"


@dataclass
class RobotStateChangedResultEvent(ResultEvent):
    robot_id: str
    new_state: CleaningMode

    def apply(self, state: RobotState, applier: "ResultEventApplier") -> RobotState:
        return applier.apply_state_changed(self, state)

    def get_event_type(self) -> str:
        return f"ROBOT_STATE_CHANGED {self.new_state.name}"


@dataclass
class RobotStartedResultEvent(ResultEvent):
    robot_id: str

    def apply(self, state: RobotState, applier: "ResultEventApplier") -> RobotState:
        return applier.apply_started(self, state)

    def get_event_type(self) -> str:
        return "ROBOT_STARTED"


@dataclass
class RobotStoppedResultEvent(ResultEvent):
    robot_id: str

    def apply(self, state: RobotState, applier: "ResultEventApplier") -> RobotState:
        return applier.apply_stopped(self, state)

    def get_event_type(self) -> str:
        return "ROBOT_STOPPED"


@dataclass
class RobotResetResultEvent(ResultEvent):
    robot_id: str

    def apply(self, state: RobotState, applier: "ResultEventApplier") -> RobotState:
        return applier.apply_reset(self, state)

    def get_event_type(self) -> str:
        return "ROBOT_RESET"


@dataclass
class ErrorResultEvent(ResultEvent):
    robot_id: str
    source_event_type: str
    message: str

    def apply(self, state: RobotState, applier: "ResultEventApplier") -> RobotState:
        return applier.apply_error(self, state)

    def get_event_type(self) -> str:
        return f"ERROR {self.source_event_type} | {self.message}"


@dataclass
class RejectedResultEvent(ResultEvent):
    robot_id: str
    source_event_type: str
    reason: str

    def get_event_type(self) -> str:
        return f"REJECTED {self.source_event_type} | {self.reason}"


class ResultEventApplier:
    def apply_moved(
        self, event: RobotMovedResultEvent, state: RobotState
    ) -> RobotState:
        angle_radians = math.radians(state.angle)
        return RobotState(
            x=state.x + event.distance * math.cos(angle_radians),
            y=state.y + event.distance * math.sin(angle_radians),
            angle=state.angle,
            state=state.state,
            is_error=state.is_error,
            error_message=state.error_message,
        )

    def apply_turned(
        self, event: RobotTurnedResultEvent, state: RobotState
    ) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=event.angle,
            state=state.state,
            is_error=state.is_error,
            error_message=state.error_message,
        )

    def apply_state_changed(
        self, event: RobotStateChangedResultEvent, state: RobotState
    ) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle,
            state=event.new_state.value,
            is_error=state.is_error,
            error_message=state.error_message,
        )

    def apply_started(
        self, event: RobotStartedResultEvent, state: RobotState
    ) -> RobotState:
        return state

    def apply_stopped(
        self, event: RobotStoppedResultEvent, state: RobotState
    ) -> RobotState:
        return state

    def apply_reset(
        self, event: RobotResetResultEvent, state: RobotState
    ) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle,
            state=state.state,
            is_error=False,
            error_message="",
        )

    def apply_error(self, event: ErrorResultEvent, state: RobotState) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle,
            state=state.state,
            is_error=True,
            error_message=event.message,
        )

    def apply_noop(self, event: ResultEvent, state: RobotState) -> RobotState:
        return state


class EventProcessor(ABC, Generic[TEvent]):
    event_type: type[TEvent]

    def handle(self, event: Event) -> List[Event]:
        self._check_event_type(event, self.event_type)
        checked_event = cast(TEvent, event)
        return self._handle(checked_event)

    def _check_event_type(self, event: Event, event_type: type[Event]) -> None:
        if not isinstance(event, event_type):
            raise TypeError(f"{type(self)} cannot handle {type(event)}")

    @abstractmethod
    def _handle(self, event: TEvent) -> List[Event]:
        pass


class DomainEventProcessor(EventProcessor[TRequestEvent], ABC):
    def __init__(self, state_provider: Callable[[str], RobotState]) -> None:
        self._state_provider = state_provider

    def _handle(self, event: TRequestEvent) -> List[Event]:
        current_state = self._state_provider(event.robot_id)
        if current_state.is_error and not isinstance(event, RobotResetRequestEvent):
            return [
                RejectedResultEvent(
                    event.robot_id, event.get_event_type(), "Robot is in error state"
                )
            ]

        error_events = self._check_domain_rules(event, current_state)
        if error_events:
            return error_events

        try:
            return self._process(event, current_state)
        except Exception as error:
            return [
                ErrorResultEvent(event.robot_id, event.get_event_type(), str(error))
            ]

    def _check_rule(self, event: Event, condition: bool, message: str) -> List[Event]:
        if condition:
            return []
        return [ErrorResultEvent(event.robot_id, event.get_event_type(), message)]

    def _check_domain_rules(
        self, event: TRequestEvent, current_state: RobotState
    ) -> List[Event]:
        return []

    @abstractmethod
    def _process(self, event: TRequestEvent, current_state: RobotState) -> List[Event]:
        pass


class MovementProcessor(DomainEventProcessor[RobotMovedRequestEvent]):
    event_type = RobotMovedRequestEvent

    def _check_domain_rules(
        self, event: RobotMovedRequestEvent, current_state: RobotState
    ) -> List[Event]:
        return self._check_rule(event, event.distance > 0, "Distance must be positive")

    def _process(
        self, event: RobotMovedRequestEvent, current_state: RobotState
    ) -> List[Event]:
        return [RobotMovedResultEvent(event.robot_id, event.distance)]


class TurnProcessor(DomainEventProcessor[RobotTurnedRequestEvent]):
    event_type = RobotTurnedRequestEvent

    def _check_domain_rules(
        self, event: RobotTurnedRequestEvent, current_state: RobotState
    ) -> List[Event]:
        return self._check_rule(
            event, 0 <= event.angle <= 360, "Angle must be in range [0, 360]"
        )

    def _process(
        self, event: RobotTurnedRequestEvent, current_state: RobotState
    ) -> List[Event]:
        return [RobotTurnedResultEvent(event.robot_id, event.angle)]


class StateChangeProcessor(DomainEventProcessor[RobotStateChangedRequestEvent]):
    event_type = RobotStateChangedRequestEvent

    def _process(
        self, event: RobotStateChangedRequestEvent, current_state: RobotState
    ) -> List[Event]:
        return [RobotStateChangedResultEvent(event.robot_id, event.new_state)]


class StartProcessor(DomainEventProcessor[RobotStartedRequestEvent]):
    event_type = RobotStartedRequestEvent

    def _process(
        self, event: RobotStartedRequestEvent, current_state: RobotState
    ) -> List[Event]:
        return [RobotStartedResultEvent(event.robot_id)]


class StopProcessor(DomainEventProcessor[RobotStoppedRequestEvent]):
    event_type = RobotStoppedRequestEvent

    def _process(
        self, event: RobotStoppedRequestEvent, current_state: RobotState
    ) -> List[Event]:
        return [RobotStoppedResultEvent(event.robot_id)]


class ResetProcessor(DomainEventProcessor[RobotResetRequestEvent]):
    event_type = RobotResetRequestEvent

    def _process(
        self, event: RobotResetRequestEvent, current_state: RobotState
    ) -> List[Event]:
        return [RobotResetResultEvent(event.robot_id)]
