from hashtable import *
from __future__ import annotations

# АТД PowerSet (расширяет HashTable)
# ограничений на количество элементов нет (таблица динамически расширяется)
# 
# Запросы: все запросы без предусловий
# intersection(self, other) - пересечение множеств
# union(self, other) -- объединение множеств
# issubset(self, other) -- является ли подмножеством
# __eq__(self, other) - совпадают ли множества
# __iter__ (self)- итератор по элементам

class PowerSet(HashTable):
    def __iter__(self):
        return iter(filter(lambda x: x != self._BUSY_SLOT and x != None, self._slots))
    
    #запросы
    def intersection(self, other: PowerSet) -> PowerSet:
        ans = PowerSet()
        for elem in other:
            if self.has_value(elem):
                ans.put(elem)
        return ans
    
    def union(self, other: PowerSet) -> PowerSet:
        ans = PowerSet()
        for elem in self:
            ans.put(elem)
        
        for elem in other:
            ans.put(elem)
        return ans
    
    def issubset(self, other: PowerSet) -> bool:
        return all(other.has_value(value) for value in self)
    
    def __eq__(self, other: PowerSet) -> bool:
        return self.issubset(other) and other.issubset(self)
