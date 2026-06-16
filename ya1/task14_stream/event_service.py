import threading
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from typing import Any, Callable, Dict, List

from base import RobotState
from events import Event, EventProcessor, ResultEvent, ResultEventApplier


class ProcessorRegistry:
    def __init__(self) -> None:
        self._subscribers: dict[type[Event], List[EventProcessor[Any]]] = {}

    def subscribe(self, processor: EventProcessor[Any]) -> None:
        handlers = self._subscribers.setdefault(processor.event_type, [])
        if processor in handlers:
            return
        handlers.append(processor)

    def get_processors_for(self, event_type: type[Event]) -> List[EventProcessor[Any]]:
        return self._subscribers.get(event_type, [])

    def get_processors(self, event: Event) -> List[EventProcessor[Any]]:
        return self.get_processors_for(type(event))


# шина
class InfrastructureEventBus:
    def __init__(self) -> None:
        self._subscribers: dict[type[Event], List[Callable[[Any], None]]] = {}

    def subscribe(
        self,
        event_type: type[Event],
        handler: Callable[[Any], None],
    ) -> None:
        handlers = self._subscribers.setdefault(event_type, [])
        if handler in handlers:
            return
        handlers.append(handler)

    def get_handlers(self, event: Event) -> List[Callable[[Any], None]]:
        handlers: List[Callable[[Any], None]] = []
        for subscribed_event_type, subscribers in self._subscribers.items():
            if isinstance(event, subscribed_event_type):
                handlers.extend(subscribers)
        return handlers

    def handle(self, event: Event) -> None:
        for handler in self.get_handlers(event):
            handler(event)


# класс - сентинел, признак штатного завершения потока
# обработки событий
@dataclass(frozen=True)
class StopDispatcherEvent(Event):
    robot_id: str = "__dispatcher__"

    def get_event_type(self) -> str:
        return "STOP_DISPATCHER"


class DispatcherState(Enum):
    RUN = "RUN"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    FAILED = "FAILED"


# кеш текущего состояния для каждого робота
# может быть вызван разными потоками как на чтение, так и на запись
# все методы -- с критическими секциями
class EventDispatcherCache:
    def __init__(
        self,
        initial_states: Dict[str, RobotState],
        applier: ResultEventApplier,
    ) -> None:
        self._lock = threading.Lock()
        self._applier = applier
        self._states = dict(initial_states)

    def check_robot_exists(self, robot_id: str) -> None:
        with self._lock:
            if robot_id not in self._states:
                raise ValueError(f"Unknown robot_id: {robot_id}")

    def get_current_state(self, robot_id: str) -> RobotState:
        self.check_robot_exists(robot_id)
        with self._lock:
            return self._states[robot_id]

    def apply_result_event(self, event: ResultEvent) -> None:
        with self._lock:
            current_state = self._states[event.robot_id]
            self._states[event.robot_id] = event.apply(current_state, self._applier)


"""
диспетчер поддерживает пул из заданного количества потоков
выполняет шардинг -- когна несколько роботов на 1 коток

"""


class EventDispatcher:
    MAX_THREADS = 5

    def __init__(
        self,
        domain_registry: ProcessorRegistry,
        infratructure_bus: InfrastructureEventBus,
    ) -> None:
        # инициализация
        self._domain_registry = domain_registry
        self._infra_bus = infratructure_bus

        # состояние жизненного цикла диспетчера
        self._state = DispatcherState.RUN

        # блокировка для записи состояния
        self._state_lock = threading.Lock()

        # сентинел и шард-очереди событий
        self._sentinel = StopDispatcherEvent()
        self._event_queues = [Queue[Event]() for _ in range(self.MAX_THREADS)]

        # пул потоков
        self._thread_pool: List[threading.Thread] = []
        self._start_threads()

    # запрос - получить индекс очереди для робота по robot_id
    def _get_shard_index(self, robot_id: str) -> int:
        if len(robot_id) == 0:
            return 0
        return ord(robot_id[-1]) % self.MAX_THREADS

    # запрос - получить очередь событий для робота по robot_id из события
    def _get_q_by_event(self, event: Event) -> Queue[Event]:
        return self._event_queues[self._get_shard_index(event.robot_id)]

    # команда - инициализация пула потоков. Выполняется на старте. Даем потокам имена чтобы не создались ошибочно дважды.
    def _start_threads(self) -> None:
        self._thread_pool = [
            threading.Thread(
                target=self._run,
                args=(event_queue,),
                name=f"thread_{thread_index}",
                daemon=True,
            )
            for thread_index, event_queue in enumerate(self._event_queues)
        ]

        for thread in self._thread_pool:
            thread.start()

    # команда -- перевести в состояние FAILED при отказе инфраструктурного процессора.
    # требует критической секции, без нее - гонка
    def _mark_failed(self) -> None:
        with self._state_lock:
            self._state = DispatcherState.FAILED

    # цикл обработки "дочерних" событий
    # чтобы не влезали другие до применения результатов первого
    def _process_event_children(self, root_event: Event) -> None:
        children_queue = [root_event]

        while children_queue:
            event = children_queue.pop(0)

            # работаем вхолостую если диспетчер в ошибке
            with self._state_lock:
                if self._state is DispatcherState.FAILED:
                    return

            # штатная работа
            for processor in self._domain_registry.get_processors(event):
                children_queue.extend(processor.handle(event))

            # при ошибках инфраструктуры ставим в ошибку сам диспетчер
            try:
                self._infra_bus.handle(event)
            except Exception:
                self._mark_failed()
                return

    # основной бесконечный цикл ожидания очередного события от одного потока
    # штатные конец цикла -- сентинел
    # если сам диспетчер в ошибке, поток "сливает" событие -- обрабатывает вхолостую
    def _run(self, event_queue: Queue[Event]) -> None:
        while True:
            event = event_queue.get()
            try:
                # штатное завершение только по сентинелу
                if event is self._sentinel:
                    break

                # сливаемся если диспетчер в ошибке
                with self._state_lock:
                    if self._state is DispatcherState.FAILED:
                        continue

                # запускаем обработку порожденных событий
                self._process_event_children(event)
            finally:
                event_queue.task_done()

    # команда - добавить событие в очердеь
    def dispatch(self, event: Event) -> None:
        with self._state_lock:
            if self._state is DispatcherState.SHUTTING_DOWN:
                raise RuntimeError("EventDispatcher is stopped")
            if self._state is DispatcherState.FAILED:
                raise RuntimeError("EventDispatcher is failed")

        self._get_q_by_event(event).put(event)

    # команда - "мягкое" завершение работы.
    def shutdown(self) -> None:
        # переключаем состояние на шатдаун
        with self._state_lock:
            if self._state is DispatcherState.SHUTTING_DOWN:
                return
            if self._state is not DispatcherState.FAILED:
                self._state = DispatcherState.SHUTTING_DOWN

        # завершаем работу очередей, кладем сентинелы
        for event_queue in self._event_queues:
            event_queue.join()

        for event_queue in self._event_queues:
            event_queue.put(self._sentinel)

        # общее завершение потоков
        for thread in self._thread_pool:
            thread.join()


# хранилище событий
class EventStore:
    def __init__(self) -> None:
        self._store: Dict[str, List[Event]] = {}
        self._lock = threading.Lock()

    def push(self, event: Event) -> None:
        with self._lock:
            event_list = self._store.setdefault(event.robot_id, [])
            event_list.append(event)

    def get_events(self, robot_id: str) -> List[Event]:
        with self._lock:
            return list(self._store.get(robot_id, []))
