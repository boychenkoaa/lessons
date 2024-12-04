from typing import TypeVar, Iterable, Generic
from enum import Enum
T = TypeVar("T")

# самодеятельность, для краткости
class CommandStatus(Enum):
    NIL = 0
    ERR = 1
    OK = 2
    
class LinkedList (Generic[T]):
    def __init__(self):
        ...
    
    @property
    def get_status(self)  -> CommandStatus:
        ...
    
    @property
    def head_status(self)  -> CommandStatus:
        ...
    
    @property
    def tail_status(self) -> CommandStatus:
        ...
    
    @property
    def right_status(self) -> CommandStatus:
        ...
    
    @property
    def put_right_status(self) -> CommandStatus:
        ...
    
    @property
    def put_left_status(self) -> CommandStatus:
        ...
    
    @property
    def remove_status(self) -> CommandStatus:
        ...
    
    @property
    def add_to_empty_status(self) -> CommandStatus:
        ...
    
    @property
    def add_tail_status(self) -> CommandStatus:
        ...
    
    @property
    def replace_status(self) -> CommandStatus:
        ...
    
    @property
    def find_status(self) -> CommandStatus:
        ...
    
    @property
    def replace_all_status(self) -> CommandStatus:
        ...
    
    def get(self) -> T:
        ...    
    
    def size(self) -> int:
        ...
        
    # предусловие: список не пуст 
    @property
    def is_head(self) -> bool:
        ...
    
    # предусловие: список не пуст
    @property
    def is_tail(self) -> bool:
        ...
    
    @property
    def is_value() -> bool:
        ...    
    
    # команды
    # предусловие: список не пуст
    # постусловие: курсор в голове
    def head(self):
        ...
    
    # предусловие: список не пуст
    # постусловие: курсор в хвосте
    def tail(self):
        ...
    
    # предусловие: список не пуст и курсор не в хвосте
    def right(self):
        ...
    
    # предусловие: список не пуст
    # постусловие: добавлен 1 элемент
    def put_right(self, new_value: T):
        ...
    
    # предусловие: список не пуст
    # постусловие: добавлен 1 элемент
    def put_left(self, new_value: T):
        ...
        
    # предусловие: список не пуст
    # постусловие: удален 1 элемент
    def remove(self):
        ...
        
    # постусловие: список пуст
    def clear():
        ...
    
    # предусловие: список пуст
    # постусловие: текущее значение = new_value и размер = 1
    def add_to_empty(self, new_value: T):
        ...
        
    # предусловие: список не пуст
    # постусловие: добавлен 1 элемент
    def add_tail(self, new_value: T):
        ...
        
    # предусловие: список не пуст
    # постусловие: текущее значение = new_value
    def replace(self, new_value: T):
        ...
    
    # предусловие: список не пуст и такое значение существует
    # постусловие: текущее значение = new_value
    def find(self, value: T):
        ...
            
    # есть ли предусловие?
    # постусловие: в спискне нет значений типа value (проверка неэффективна)
    def remove_all(self, value: T):
        ...
