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
    
# АТД Словарь для строк
# тут будет очень уместен курсор (неявный)
class NativeDictionary:
    def __init__(self):
        self._BUSY_SLOT = -1
        self._size = 17
        self._step = 2
        self.clear()
    
    # запросы, все без предусловий
    # внутренний запрос - валидный ли ключ
    def _is_valid_key(self, key: str) -> bool:
        return key != None and key != self._BUSY_SLOT
        
    # статус запроса "чернового" поиска -- сомнительно (сам seek приватен), но ОК
    @property
    def seek_status(self):
        return self._seek_status

    # статус команды удаления элемента
    @property
    def remove_status(self) -> Status:
        return self._remove_status    

    # хеш функция
    def _hash(self, value: str) -> int:
        if value == "":
            return 0
        ans = ord (value[0]) % self.size
        return ans

    # запрос -- есть ли ключ
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

    # внутренняя команда
    # установить курсор на первое подходящее незанятое место
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
    
    # рехеширование
    def _rehash(self):
        self._size = self._size * 2 + 1
        old_keys = copy(self._keys)
        old_values = copy(self._values)
        self.clear()
        for old_key, old_value in filter(lambda k, v: self._is_valid_key(k), zip(old_keys, old_values)):
            self.update(old_key, old_value)    

    # команда -- удалить пару ключ-значение
    # предусловие: ключ есть
    # постусловие -- ключа нет (удален)
    def remove(self, key: str):
        self._seek(key)
        if self._seek_status != SeekStatus.EXIST:
            self._remove_status = Status.ERR
            return
    
        self._keys[self._cursor] = self._BUSY_SLOT
        self._remove_status = Status.OK

    # команда -- обновить пару ключ-значение
    # предусловий нет (если ключ есть, значение перезаписывается)
    # при переполнении делаем рехэширование
    def update(self, key: str, value: str):
        self._seek(key)
        if self._seek_status == SeekStatus.OVERFLOW:
            self._rehash()
            self._seek(key)
        
        self._keys[self._cursor] = key
        self._values[self._cursor] = value
