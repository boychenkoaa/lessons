from typing import Dict, List

from base import RobotState
from commands import Command, CommandHandler
from event_service import (
    EventDispatcher,
    EventDispatcherCache,
    EventStore,
    InfrastructureEventBus,
    ProcessorRegistry,
)
from events import (
    ErrorResultEvent,
    Event,
    MovementProcessor,
    RejectedResultEvent,
    ResetProcessor,
    ResultEventApplier,
    RobotMovedRequestEvent,
    RobotMovedResultEvent,
    RobotResetRequestEvent,
    RobotResetResultEvent,
    RobotStartedRequestEvent,
    RobotStartedResultEvent,
    RobotStateChangedRequestEvent,
    RobotStateChangedResultEvent,
    RobotStoppedRequestEvent,
    RobotStoppedResultEvent,
    RobotTurnedRequestEvent,
    RobotTurnedResultEvent,
    StartProcessor,
    StateChangeProcessor,
    StopProcessor,
    TurnProcessor,
)
from time_travel import TimeTraveler

_REQUEST_EVENT_TYPES = [
    RobotMovedRequestEvent,
    RobotTurnedRequestEvent,
    RobotStateChangedRequestEvent,
    RobotStartedRequestEvent,
    RobotStoppedRequestEvent,
    RobotResetRequestEvent,
]

_RESULT_EVENT_TYPES = [
    RobotMovedResultEvent,
    RobotTurnedResultEvent,
    RobotStateChangedResultEvent,
    RobotStartedResultEvent,
    RobotStoppedResultEvent,
    RobotResetResultEvent,
    ErrorResultEvent,
    RejectedResultEvent,
]

_DOMAIN_PROCESSORS = [
    MovementProcessor,
    TurnProcessor,
    StateChangeProcessor,
    StartProcessor,
    StopProcessor,
    ResetProcessor,
]


class Application:
    def __init__(self, initial_states: Dict[str, RobotState]) -> None:
        # инициализация "базовой" инфраструктуры
        self._initial_states = dict(initial_states)
        self._applier = ResultEventApplier()
        self._event_store = EventStore()
        self._event_log = EventStore()
        self._cache = EventDispatcherCache(self._initial_states, self._applier)
        self._command_handler = CommandHandler()

        self._time_traveler = TimeTraveler(
            self._event_store, self._applier, self._initial_states
        )

        # настройка доменных подписок
        domain_registry = ProcessorRegistry()
        state_provider = self._cache.get_current_state
        for processor_cls in _DOMAIN_PROCESSORS:
            domain_registry.subscribe(processor_cls(state_provider))

        # настройка инфраструктурных подписок
        # хранилище и лог
        infra_bus = InfrastructureEventBus()

        all_event_types = _REQUEST_EVENT_TYPES + _RESULT_EVENT_TYPES
        for event_type in all_event_types:
            infra_bus.subscribe(event_type, self._event_log.push)

        for event_type in _RESULT_EVENT_TYPES:
            infra_bus.subscribe(event_type, self._event_store.push)
            infra_bus.subscribe(event_type, self._cache.apply_result_event)

        # инициализация самой инфраструктуры
        self._dispatcher = EventDispatcher(domain_registry, infra_bus)

    # основная команда
    def handle_command(self, robot_id: str, command: Command) -> None:
        current_state = self._cache.get_current_state(robot_id)
        for event in self._command_handler.handle_command(
            robot_id, command, current_state
        ):
            self._dispatcher.dispatch(event)

    # команда на завершение работы. дальше только просмотр истории
    def shutdown(self) -> None:
        self._dispatcher.shutdown()

    # запрос - текущее состояние
    def get_state(self, robot_id: str) -> RobotState:
        return self._cache.get_current_state(robot_id)

    # запрос - все события по айди робота
    def get_events(self, robot_id: str) -> List[Event]:
        return self._event_store.get_events(robot_id)

    def get_state_after(self, robot_id: str, event_index: int) -> RobotState:
        return self._time_traveler.get_state_after(robot_id, event_index)

    def undo(self, robot_id: str, event_index: int) -> RobotState:
        return self._time_traveler.undo(robot_id, event_index)

    @property
    def event_log(self) -> EventStore:
        return self._event_log
