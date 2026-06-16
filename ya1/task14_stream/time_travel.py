from copy import copy
from typing import Dict, Iterator, List, Tuple

from base import RobotState
from event_service import EventStore
from events import Event, ResultEvent, ResultEventApplier

# перемещение по истории событий и их применение
class TimeTraveler:
    def __init__(
        self,
        event_store: EventStore,
        applier: ResultEventApplier,
        initial_states: Dict[str, RobotState],
    ) -> None:
        self._event_store = event_store
        self._applier = applier
        self._initial_states = dict(initial_states)

    def _events(self, robot_id: str) -> List[Event]:
        return self._event_store.get_events(robot_id)

    def _replay(self, robot_id: str, count: int) -> RobotState:
        state = copy(self._initial_states[robot_id])
        for event in self._events(robot_id)[:count]:
            if isinstance(event, ResultEvent):
                state = event.apply(state, self._applier)
        return state

    def get_state_after(self, robot_id: str, event_index: int) -> RobotState:
        events = self._events(robot_id)
        count = max(0, min(event_index + 1, len(events)))
        return self._replay(robot_id, count)

    def undo(self, robot_id: str, event_index: int) -> RobotState:
        events = self._events(robot_id)
        count = max(0, min(event_index, len(events)))
        return self._replay(robot_id, count)
