from typing import TypeVar, Generic
from parent_list import TwoWayList, Status

# АТД Базовой очереди

T = TypeVar("T")
class QueueBase(Generic[T]):
    def __init__(self):
        self._q_status = Status.NIL
        self._c_status = Status.NIL
        self._li = TwoWayList[T]
    
    # запросы
    # длина очереди
    @property
    def size(self):
        return self._li.size
    
    # статус последнего запроса с предусловием
    @property
    def q_status(self) -> Status:
        return self._q_status
       
    # статус последней команды с предусловием
    @property 
    def c_status(self) -> Status:
        return self._c_status

    # пуста ли очередь
    @property     
    def is_empty(self) -> bool:
        return self._li.is_value
    
    # запрос - получить первое значение
    # предусловие: не пуст
    @property    
    def get_head(self) -> T:
        self._li.head
        if self._li.head_status == Status.ERR:
            self._q_status = Status.ERR
            return None
        ans = self._li.get
        if self._li.get_status == Status.ERR:
            self._q_status = Status.ERR
            return None        
        return ans
    
    # запрос - получить последнее значение
    # предусловие: не пуст    
    @property
    def get_tail(self) -> T:
        self._li.tail
        if self._li.tail_status == Status.ERR:
            self._q_status = Status.ERR
            return None
        ans = self._li.get
        if self._li.get_status == Status.ERR:
            self._q_status = Status.ERR
            return None        
        return ans
        
    # команда - удалить первое значение
    # предусловие: не пуст
    # постусловие -- удален  1 элемент
    def delete_head(self):
        self._li.head
        if self._li.head_status == Status.ERR:
            self._c_status = Status.ERR
            return
        self._li.remove
        self._c_status = self._li.remove_status
        
    # команда добавить в хвост
    # без предусловий
    # постусловие -- в хвост добавлен 1 элемент
    def add_to_tail(self, new_value: T):
        if self.is_empty:
            self._li.add_to_empty(new_value)
            self._c_status = self._li.add_to_empty_status
            return
        
        self._li.add_tail(new_value)
        self._c_status = self._li.add_tail_status
        
    # команда очистки дека
    # постусловие -- дек пустой
    def clear(self):
        self._li.clear()
        
# обычная очередь это просто алиас
Queue = QueueBase

# АТД Дек
class Deque(QueueBase):
    def __init__(self):
        super().__init__()
        
    # команда - удалить последний элемент
    # предусловие: не пуст
    # постусловие -- удален 1 элемент
    def delete_tail(self):
        self._li.tail
        if self._li.tail_status == Status.ERR:
            self._c_status = Status.ERR
            return
        self._li.remove
        self._c_status = self._li.remove_status
        
    # команда - добавить элемент в начало
    # постусловие -- добавлен 1 элемент
    def add_to_head(self, new_value: T):
        if self.is_empty:
            self._li.add_to_empty(new_value)
            self._c_status = self._li.add_to_empty_status
            return
        
        self._li.put_left(new_value)
        self._c_status = self._li. put_left_status
