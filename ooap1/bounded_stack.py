from functools import reduce

DEFAULT_STACK_CAPACITY = 32

class BoundedStack:
    def __init__(self, capacity: int = DEFAULT_STACK_CAPACITY):
        self._POP_NIL = 0
        self._POP_OK = 1
        self._POP_ERR = 1
        self._PEEK_NIL = 0
        self._PEEK_OK = 1
        self._PEEK_ERR = 2
        self._PUSH_NIL = 0
        self._PUSH_OK = 1
        self._PUSH_ERR = 2
        self._capacity = capacity
        self.clear()
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    @property
    def POP_NIL(self):
        return self._POP_NIL
    
    @property
    def POP_OK(self):
        return self._POP_OK
    
    @property
    def POP_ERR(self):
        return self._POP_ERR
    
    @property
    def PUSH_NIL(self):
        return self._PUSH_NIL
    
    @property
    def PUSH_OK(self):
        return self._PUSH_OK
    
    @property
    def PUSH_ERR(self):
        return self._PUSH_ERR        
    
    @property
    def PEEK_NIL(self):
        return self._PEEK_NIL
    
    @property
    def PEEK_OK(self):
        return self._PEEK_OK
    
    @property
    def PEEK_ERR(self):
        return self._PEEK_ERR

    @property
    def size(self):
        return len(self._stack)
    
    @property
    def pop_status(self):
        return self._pop_status
    
    @property
    def peek_status(self):
        return self._peek_status

    def pop(self):
        if self.size == 0:
            self._pop_status = self.POP_ERR
        else:
            self._pop_status = self.POP_OK
            self._stack.pop(-1)

    def push(self, value):
        if self.size < self.capacity:
            self._stack.append(value)
            self._push_status = self.PUSH_OK
        else:
            self._push_status = self.PUSH_ERR

    @property
    def peek(self):
        if self.size == 0:
            ans = None
            self._peek_status = self.PEEK_ERR
        else:
            ans = self._stack[-1]
            self._peek_status = self.PEEK_OK
        return ans
    
    def clear(self):
        self._stack = []
        self._peek_status = self.PEEK_NIL
        self._pop_status = self.POP_NIL
        self._push_status = self.PUSH_NIL

    def __str__(self):
        return reduce(lambda x, y: x + ' '+ y, map(str, self._stack[::-1]) )
