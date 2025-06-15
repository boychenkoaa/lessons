from __future__ import annotations
from general import General, Any, Void
from typing import TypeVar, Generic

class Additive(Any):
    def __add__(self, other: Any):
        raise NotImplementedError

    def __radd__(self, other: Any):
        raise NotImplementedError
    
_T = TypeVar('_T', bound='Additive')

class Vector(Generic[_T], Additive):
    APPEND_NIL = 0
    APPEND_OK = 1
    APPEND_WARNING = 2
    APPEND_ERROR = 3
    GET_ITEM_NIL = 0
    GET_ITEM_OK = 1
    GET_ITEM_WARNING = 2
    GET_ITEM_ERROR = 3
    SET_ITEM_NIL = 0
    SET_ITEM_OK = 1
    SET_ITEM_WARNING = 2
    SET_ITEM_ERROR = 3
    ADD_NIL = 0
    ADD_OK = 1
    ADD_WARNING = 2
    ADD_ERROR = 3
    
    def __init__(self, length: int = 0):
        self._li = [Void] * length
        self._append_status = self.APPEND_NIL
        self._get_item_status = self.GET_ITEM_NIL
        self._set_item_status = self.SET_ITEM_NIL
        self._add_status = self.ADD_NIL
    
    def __len__(self):
        return len(self._li)
    
    def append(self, value: _T):
        self._li.append(value)
        self._append_status = self.APPEND_OK

    def get_append_status(self) -> int:
        return self._append_status

    def get_get_item_status(self) -> int:
        return self._get_item_status

    def get_set_item_status(self) -> int:
        return self._set_item_status

    def get_add_status(self) -> int:
        return self._add_status
    
    def __getitem__(self, index: int) -> _T:
        if index >= len(self) or index < 0:
            self._get_item_status = self.GET_ITEM_ERROR
            return Void
        
        self._get_item_status = self.GET_ITEM_OK
        return self._li[index]
    
    def __setitem__(self, index, value):
        if index >= len(self) or index < 0:
            self._set_item_status = self.SET_ITEM_ERROR
            return

        self._set_item_status = self.SET_ITEM_OK
        self._li[index] = value
        
    def __add__(self, other: Vector[_T]) -> Vector[_T]:
        N = len(self)
        if N != len(other):
            self._add_status = self.ADD_ERROR
            return Void
        
        ans = Vector[_T](N)
        for i in range(N):
            ans[i] = self[i] + other[i]

        self._add_status = self.ADD_OK
        return ans

    def __radd__(self, other: Vector[_T]) -> Vector[_T]:
        return self.__add__(other)

if __name__ == '__main__':
    v1 = Vector[int](3)
    v2 = Vector[int](3)
    v1[0] = 1
    v1[1] = 2
    v1[2] = 3
    v2[0] = 4
    v2[1] = 5
    v2[2] = 6
    v3 = v1 + v2
    print(v3[0], v3[1], v3[2])
    print(v1.get_add_status())
