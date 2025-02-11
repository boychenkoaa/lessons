from __future__ import annotations
from copy import deepcopy
from enum import Enum

BLOOM_FILTER_SIZE = 32

class Status(Enum):
    NIL = 0
    ERR = 1
    OK = 2

# АТД BloomFilter 
# фильтр Блума для строковых значений

class SimpleBloomFilter:
    def __init__(self):
        self._size = BLOOM_FILTER_SIZE
        self._counts = [0] * self._size
        self._remove_status = Status.NIL
    
    # запросы, все без предусловий
    
    # массив значений по индексам
    @property
    def counts(self):
        return deepcopy(self._counts)
    
    # хеш
    def _hash17(self, s: str) -> int:
        # 17
        ans = sum((17 * ans + ord(c)) % self._size for c in s)
        return ans        

    # хеш
    def _hash223(self, s: str) -> int:
        # 223 
        ans = sum((17 * ans + ord(c)) % self._size for c in s)
        return ans        

    # запрос - кортеж из хешей-индексов, где нужно увеличить на 1
    def _hash_tuple(self, s: str) -> int:
        return (self._hash17(s), self._hash223(s))
    
    # проверка значения на вхождение
    def is_value(self, s: str) -> bool:
        return all(self.counts[i] > 0 for i in self._hash_tuple(s))
             
    # далее идут команды
    # добавление элемента в фильтр
    def add(self, s: str):
        for i in self._hash_tuple(s):
            self.counts[i] += 1        

    # слияние с другим фильтро
    def merge_with(self, other: SimpleBloomFilter):
        self._counts = [x + y for x, y in zip (self.counts, other.counts)]
    
    # предусловие: удаляемый есть
    # удаление элемента
    def remove(self, s: str):
        if not self.is_value(s):
            self._remove_status = Status.ERR
            return 
        
        for i in self._hash_tuple(s):
            self.counts[i] -= 1
    
    # очистка
    def clear(self):
        self._counts = [0] * self._size
        self._remove_status = Status.NIL
        
