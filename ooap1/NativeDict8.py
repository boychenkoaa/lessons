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
    
# тут очень уместен курсор
class NativeDictionary:
    def __init__(self):
        self._BUSY_SLOT = -1
        self._size = 17
        self._step = 2
        self.clear()
    
    # запросы, все без предусловий
    def is_valid_key(self, key) -> bool:
        return key != None and key != self._BUSY_SLOT
        
    @property
    def seek_status(self):
        return self._seek_status
    

    @property
    def remove_status(self) -> Status:
        return self._remove_status    
    
    def _hash(self, value: str) -> int:
        if value == "":
            return 0
        ans = ord (value[0]) % self.size
        return ans

    def has_key(self, key: str) -> bool:
        self._seek(key)
        return self._seek_status == SeekStatus.EXIST    
    
  # мягкий вариант без предусловий
    def get(self, key: str) -> str:
        self._seek(key)
        if self.seek_status != SeekStatus.EXIST:
            return None
        return self._keys[self._cursor]
    
    # команды
    def clear(self):
        self._keys = [None] * self._size
        self._values = [None] * self._size
        self._seek_status = SeekStatus.NIL
        self._cursor = None
        self._remove_status = Status.NIL
    
    # искать подходящее незанятое место, установить seek на него
    # предусловие -- место существует
    def _seek(self, key: str):
        self._cursor = self._hash(key)
        start_index = self._cursor
        self._seek_status = SeekStatus.EMPTY
        while self._keys[self._cursor] != None:
            self._cursor = (self._cursor + self._step) % self._size
            if self._cursor == start_index:
                self._seek_status = SeekStatus.OVERFLOW
                return
            
            if self._keys[self._cursor] == key:
                self._seek_status = SeekStatus.EXIST
                return
        
    def _rehash(self):
        self._size = self._size * 2 + 1
        old_keys = copy(self._keys)
        old_values = copy(self._values)
        self.clear()
        for old_key, old_value in filter(lambda k, v: self.is_valid_key(k), zip(old_keys, old_values)):
            self.update(old_key, old_value)    
    
    # предусловие: ключ есть
    def remove(self, key: str):
        self._seek(key)
        if self._seek_status != SeekStatus.EXIST:
            self._remove_status = Status.ERR
            return
    
        self._keys[self._cursor] = self._BUSY_SLOT
        self._remove_status = Status.OK
            
    # предусловий нет
    # при переполнении делаем рехэширование
    def update(self, key: str, value: str):
        self._seek(key)
        if self._seek_status == SeekStatus.OVERFLOW:
            self._rehash()
            self._seek(key)
        
        self._keys[self._cursor] = key
        self._values[self._cursor] = value
