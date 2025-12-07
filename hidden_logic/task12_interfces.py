from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from typing import Callable, Generic, Iterator, List, TypeVar, override

"""
приведу мой базовый модуль для персистентных коллекций
интерфейсы помогают подменять разные реализации по необходимости
"""

T = TypeVar("T")


class Collection(Generic[T], ABC):
    def __init__(self): ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __iter__(self) -> Iterator[T]: ...

    @abstractmethod
    def __contains__(self, item: T) -> bool: ...

    @abstractmethod
    def clear(self) -> None: ...

    def is_empty(self) -> bool:
        return len(self) == 0

    def is_not_empty(self) -> bool:
        return not self.is_empty()

    def find_first(self, predicate: Callable[[T], bool]) -> T:
        ans = next((item for item in self if predicate(item)), None)
        assert ans is not None, "No item found"
        return ans

    def find_all(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self if predicate(item)]


class CollectionCommand:
    def __init__(self, collection: Collection[T]):
        self._collection = collection

    def collection_is(self, other: Collection[T]) -> bool:
        return self._collection == other

    @abstractmethod
    def execute(self): ...


class InvertibleCommand(CollectionCommand):
    def __init__(self, collection: Collection[T]):
        super().__init__(collection)

    # запрос -- не меняет состояния!
    # возвращает обратную команду
    # команда остается как была
    @abstractmethod
    def invert(self) -> InvertibleCommand: ...


class IdentityCommand(InvertibleCommand):
    def __init__(self, collection: Collection[T]):
        super().__init__(collection)

    def invert(self) -> IdentityCommand:
        return self

    def execute(self):
        pass


class History:
    def __init__(self): ...

    def is_empty(self) -> bool: ...

    def push(self, Command: InvertibleCommand): ...

    def pop(self) -> InvertibleCommand: ...

    def undo(self) -> None: ...

    def redo(self) -> None: ...

    def clear(self) -> None: ...

    def undo_top(self) -> InvertibleCommand: ...

    def redo_top(self) -> InvertibleCommand: ...

    def is_overflowed(self) -> bool: ...


class PersistentCollection(Generic[T]):
    def __init__(self, base_collection: Collection[T], history: History):
        super().__init__()
        self._base_collection = base_collection
        self._history = history

    def __len__(self):
        return len(self._base_collection)

    def __iter__(self):
        return iter(self._base_collection)

    def __contains__(self, item: T):
        return item in self._base_collection

    def clear(self):
        self._base_collection.clear()
        self._history.clear()

    def is_empty(self) -> bool:
        return self._base_collection.is_empty()

    def execute_command(self, collection_command: CollectionCommand):
        collection_command.execute()
        self._history.clear()

    def execute_inversible_command(self, inv_command: InvertibleCommand):
        inv_command.execute()
        self._history.push(inv_command)

    def undo(self):
        command = self._history.undo_top()
        inversed_command = command.invert()
        inversed_command.execute()
        self._history.undo()

    def redo(self):
        command = self._history.redo_top()
        command.execute()
        self._history.redo()


class TwoStackHistory(History):
    def __init__(self):
        super().__init__()
        self._undo_stack = deque()
        self._redo_stack = deque()

    def undo_top(self):
        return self._undo_stack[-1]

    def redo_top(self) -> InvertibleCommand:
        return self._redo_stack[-1]

    def redo(self):
        command = self._redo_stack.pop()
        self._undo_stack.append(command)

    def undo(self) -> None:
        command = self._undo_stack.pop()
        self._redo_stack.append(command)

    def is_overflowed(self) -> bool:
        return False


class TwoStackBoundedHistory(TwoStackHistory):
    def __init__(self, max_size: int):
        super().__init__()
        self._max_size = max_size

    @override
    def push(self, Command: InvertibleCommand):
        if self.is_overflowed():
            self._undo_stack.popleft()
        super().push(Command)

    def is_overflowed(self) -> bool:
        return len(self._undo_stack) >= self._max_size
