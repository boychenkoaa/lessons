from typing import TypeVar, Generic
from parent_list import TwoWayList, Status

# АТД Queue - очередь
T = TypeVar("T")
class Queue(Generic[T]):
    def __init__(self):
        self._q_status = Status.NIL
        self._c_status = Status.NIL
        self._li = TwoWayList[T]
    
    # запросы без предусловий

    # размер очереди
    @property
    def size(self):
        return self._li.size
    
    # статус последнего запроса с предусловием
    @property
    def q_status(self):
        return self._q_status

    # статус последней команды с предусловием
    @property 
    def c_status(self):
        return self._c_status

    # пустая ли очередь
    @property     
    def is_empty(self) -> bool:
        return self._li.is_value
    
    # запрос на первый элемент очереди
    # предусловие: очередь не пуста
    @property    
    def first(self) -> T:
        self._li.head
        if self._li.head_status == Status.ERR:
            self._q_status = Status.ERR
            return None
        ans = self._li.get
        if self._li.get_status == Status.ERR:
            self._q_status = Status.ERR
            return None        
        return ans

    # запрос на последний элемент очереди
    # предусловие: не пуст    
    @property
    def last(self) -> T:
        self._li.tail
        if self._li.tail_status == Status.ERR:
            self._q_status = Status.ERR
            return None
        ans = self._li.get
        if self._li.get_status == Status.ERR:
            self._q_status = Status.ERR
            return None        
        return ans

    # удалить элемент из хвоста очереди
    # команда, предусловие: не пуст
    # постусловие -- удален 1 элемент
    def pop(self):
        self._li.head
        if self._li.head_status == Status.ERR:
            self._c_status = Status.ERR
            return
        self._li.remove
        self._c_status = self._li.remove_status

    # команда 
    # положить элемент в голову очереди
    # постусловие -- добавлен 1 элемент
    def push(self, new_value: T):
        if self.is_empty:
            self._li.add_to_empty(new_value)
            self._c_status = self._li.add_to_empty_status
            return
        
        self._li.add_tail(new_value)
        self._c_status = self._li.add_tail_status
        
    # команда 
    # постусловие -- очередь пуста
    def clear(self):
        self._li.clear()
