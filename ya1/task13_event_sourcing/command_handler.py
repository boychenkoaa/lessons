from copy import deepcopy
from base import Status
from typing import Callable, Sequence

from pure_robot import RobotState
from robot_commands import Cmd, compose
# класс стека событий
# инвариант: курсор всегда от 0 до N-1 включительно
# курсор (текущий индекс) элемента нужен для дальнейшей реализации undo / redo
class EventStore:
    def __init__(self):
        self.clear()

    # команды базовые
    # команда - сброс статусов
    def _init_status(self):
        self._inc_status = Status.NIL
        self._dec_status = Status.NIL

    # команда - очистка очереди и сбро
    def clear(self) -> None:
        self._store = []
        self._cursor = -1
        self._init_status()

    # команда - обрезка до курсора включительно
    # предусловий нет
    # постусловие - курсор в конце
    def _trim_to_cursor(self) -> None:
        self._store = self._store[0 : self._cursor + 1]

    # команда - сдвинуть влево
    # предусловие - можем сдвинуть влево
    def dec(self) -> None:
        if self.can_dec:
            self._cursor -= 1
            self._dec_status = Status.OK
            return
        self._dec_status = Status.ERR

    # команда - сдвинуть вправо
    # предусловие - можем сдвинуть влево
    def inc(self) -> None:
        if self.can_inc:
            self._cursor += 1
            self._dec_status = Status.OK
            return

        self._inc_status = Status.ERR

    # команда -- добавить команду в очередь
    def push(self, robot_cmd: Cmd) -> None:
        # освобождаем память от курсора до конца
        self._trim_to_cursor()

        # добавляем в конец текущей истории
        self._store.append(robot_cmd)
        self.inc()

    # запрос
    def inc_status(self) -> Status:
        return self._inc_status
    
    # запрос
    def dec_status(self) -> Status:
        return self._dec_status

    # запрос
    @property
    def composition(self) -> Cmd:
        return compose(self.trimmed)

    # запрос - длина
    @property
    def count(self):
        return len(self._store)

    # запрос - можно ли сдвинуть влево
    @property
    def can_dec(self) -> bool:
        return self._cursor > 0

    # запрос - можно ли сдвинуть вправо
    @property
    def can_inc(self) -> bool:
        return self._cursor < self.count - 1

    # запрос - последовательность команд до курсора
    @property
    def trimmed(self) -> Sequence[Cmd]:
        return deepcopy(self._store[0 : self._cursor + 1])

# хендлер команд, как в задании
# 
class CommandHandler:
    def __init__(self, event_store: EventStore, initial_state: RobotState):
        self._event_store = event_store
        self._initial_state = initial_state
        self._init_status()
        
    # команда
    def _init_status(self) -> None:
        self._undo_status = Status.NIL
        self._redo_status = Status.NIL

    # запрос
    @property
    def count(self) -> int:
        return self._event_store.count
        
    # запрос
    def undo_status(self) -> Status:
        return self._undo_status
        
    # запрос
    def redo_status(self) -> Status:
        return self._redo_status
    
    # запрос
    @property
    def can_undo(self) -> bool:
        return self._event_store.can_dec
    
    @property
    def can_redo(self) -> bool:
        return self._event_store.can_inc
        
    # команда
    # применить последовательность команд от начала до курсора
    def _apply(self) -> RobotState:
        composition_cmd = self._event_store.composition
        return composition_cmd(self._initial_state)

    # команда
    # запустить команду робота
    def run(self, robot_cmd: Cmd) -> RobotState:
        # добавить в хранилище
        self._event_store.push(robot_cmd)

        # применить композицию
        return self._apply()
    
    # команда
    # предусловие -- undo возможно
    def undo(self) -> RobotState:
        # курсор влево и применить
        self._undo_status = Status.ERR
        if self.can_undo:
            self._event_store.dec()
            self._undo_status = Status.OK
        return self._apply()

    # команда - вернуть последнюю команду робота
    # предусловие -- redo возможно
    def redo(self) -> RobotState:
        self._redo_status = Status.ERR
        if self.can_redo:
            self._event_store.inc()
            self._redo_status = Status.OK
        return self._apply()