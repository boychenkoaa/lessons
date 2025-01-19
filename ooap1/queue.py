from typing import TypeVar, Generic
from parent_list import TwoWayList, Status

T = TypeVar("T")

class Queue(Generic[T]):
    def __init__(self):
        self._q_status = Status.NIL
        self._c_status = Status.NIL
        self._li = TwoWayList[T]
    
    # запросы без предусловий
    @property
    def size(self):
        return self._li.size
    
    @property
    def q_status(self):
        return self._q_status
       
    @property 
    def c_status(self):
        return self._c_status
    
    @property     
    def is_empty(self):
        return self._li.is_value
    
    # запрос, предусловие: не пуст
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
    
    # запрос, предусловие: не пуст    
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
        
    # команда, предусловие: не пуст
    def pop(self):
        self._li.head
        if self._li.head_status == Status.ERR:
            self._c_status = Status.ERR
            return
        self._li.remove
        self._c_status = self._li.remove_status
        
    # команда без предусловий
    def push(self, new_value: T):
        if self.is_empty:
            self._li.add_to_empty(new_value)
            self._c_status = self._li.add_to_empty_status
            return
        
        self._li.add_tail(new_value)
        self._c_status = self._li.add_tail_status
        
    # команда без условий
    def clear(self):
        self._li.clear()
