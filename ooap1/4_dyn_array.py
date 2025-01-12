import ctypes
from typing import TypeVar, Generic
from enum import Enum

T = TypeVar("T")
# я позволю себе не заводить разные статусы на разные операции
# сделаю 2 статуса -- для последней команды и для последнего запроса
# во встроенном итераторе пользы не вижу, у нас как раз массив -- не делаем

class Status(Enum):
    NIL = 0
    ERR = 1
    OK = 2

START_ARRAY_CAPACITY = 16
DYN_ARRAY_RESIZE_COEF = 2

class DynArray(Generic[T]):
    def __init__(self):
        self.clear()
    
    @property
    def count(self) :
        return self._count
    
    def __len__(self):
        return self.count

    def clear(self):
        self._count = 0
        self._capacity = START_ARRAY_CAPACITY
        self._array = START_ARRAY_CAPACITY * [0]
        self._command_status = Status.NIL
        self._query_status = Status.NIL        
        
    @property
    def command_status(self):
        return self._command_status

    @property
    def query_status(self):
        return self._query_status    

    @property
    def capacity(self):
        return self._capacity 

    # предусловие -- индекс в диапазоне
    def __getitem__(self, index: int):
        if index >= self._count or index < 0:
            self._query_status = Status.ERR
            return None
        self._query_status = Status.OK
        return self._array[index]
        
    # предусловий нет
    def find(self, value: T) -> int | None:
        for i in range(self.count):
            if self._array[i] == value:
                return i
        return None    
    
    def _resize(self, new_capacity: int):
        """
        предусловие -- новый размер => count
        """
        if new_capacity < self.count:
            self._command_status = Status.ERR
            return 
        
        new_array = [0] * new_capacity
        for i in range(self.count):
            new_array[i] = self._array[i]
        
        self._array = new_array
        self._capacity = new_capacity
        self._command_status = Status.OK
    
    def append(self, itm: T):
        """
        добавляет в конец
        предусловий нет, добавить в конец можно всегда
        постусловие - добавлен 1 элемент
        """
        if self.count == self.capacity:
            self._resize(2*self.capacity)
            if self._command_status == Status.ERR:
                return 
        self._array[self.count] = itm
        self._count += 1

    # предусловие: 0 <= i <= count
    def insert(self, i: int, itm: T):
        if (i < 0) or (i > self.count):
            self._command_status = Status.ERR
            return
        if self.count == self.capacity:
            self._resize(DYN_ARRAY_RESIZE_COEF*self.capacity)
            if self._command_status == Status.ERR:
                return
            
        for index in range(self.count, i, -1):
            self._array[index] = self._array[index-1]
        self._array[i] = itm
        self._count += 1
        self._command_status = Status.OK
    
    # предусловие: 0 <= i <= count
    def pop(self, i):
        if i < 0 or i > self.count:
            self._command_status = Status.ERR
            return   
        
        for index in range(i, self.count):
            self._array[index] = self._array[index+1]
        
        self._array[self.count-1] = None
        self._count -= 1
        
        if self.count < 0.5 * self.capacity:
            self._resize(max(16, int(self.capacity / 1.5)))
            if self._command_status == Status.ERR:
                return
        self._command_status = Status.OK
        
    
    # предусловие: элемент существует
    # постусловие: стало меньше на 1 элемент
    def remove(self, value: T):
        i = self.find(value)
        if i == None:
            self._command_status = Status.ERR
        self.pop(i)
        self._command_status = Status.OK
        
