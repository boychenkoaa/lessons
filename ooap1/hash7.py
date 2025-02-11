from enum import Enum
from copy import copy

class Status(Enum):
    NIL = 0
    ERR = 1
    OK = 2

class SeekStatus(Enum):
    NIL = 0
    EMPTY = 1
    OVERFLOW = 2
    EXIST = 3
    
class HashTable:
    def __init__(self, size: int):
        self._size = size if size % 2 == 1 else size + 1
        self._step = 2
        self._slots = [None] * self.size
        self._seek_status = SeekStatus.NIL
        self._put_status = Status.NIL
        self._remove_status = Status.NIL
        self._BUSY_SLOT = -1
    
    # статус команды добавления
    @property
    def put_status(self) -> Status:
        return self._put_status

    # статус команды удаления
    @property
    def remove_status(self) -> Status:
        return self._remove_status    

    # хеш функция
    def _hash(self, value: str) -> int:
        if value == "":
            return 0
        ans = ord (value[0]) % self.size
        return ans

    # поиск места для элемента "черновой"
    def _seek(self, value: str) -> int:
        index = self._hash(value)
        start_index = index
        while self._slots[index] != None:
            index = (index + self._step) % self.size
            if index == start_index:
                self._seek_status = SeekStatus.OVERFLOW
                return None                
            
            if self._slots[index] == value:
                self._seek_status = SeekStatus.EXIST
                return None
        
        self._seek_status = SeekStatus.EMPTY
        return index

    # запрос -- есть ли значение
    def has_value(self, value: str) -> bool:
        self._seek(value)
        return self._seek_status == SeekStatus.EXIST    

    # рехеширование
    def _rehash(self):
        self.size = self.size * 2 + 1
        old_slots = copy(self._slots)
        self._slots = [None] * self.size
        for value in old_slots:
            if value != None and value != self._BUSY_SLOT:
                self.put(value)    
    
    # команды
    
    # команда -- удалить элемент
    # предусловие -- value есть
    # постусловие -- удален 1 элемент
    def remove(self, value: str):
        index = self._seek(value)
        if self._seek_status != SeekStatus.EXIST:
            self._remove_status = Status.ERR
            return
    
        self._slots[index] = self._BUSY_SLOT
        self._remove_status = Status.OK
            
    
    # команда -- добавить элемент
    # предусловие: элемента нет
    # постусловие -- добавлен 1 элемент
    def put(self, value: str):
        index = self._seek(value)
        if self._seek_status == SeekStatus.EXIST:
            self._put_status = Status.ERR
            return
        
        if self._seek_status == SeekStatus.OVERFLOW:
            self._rehash()
            index = self._seek(value)
        
        self._slots[index] = value
        self._put_status = Status.OK
