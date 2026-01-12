class Deque:
    def __init__(self):
        self._arr = []

    def addFront(self, item):
        # добавление в голову
        self._arr.insert(0, item)

    def addTail(self, item):
        # добавление в хвост
        self._arr.append(item)

    def removeFront(self):
        # удаление из головы
        if not self._arr:
            return None
        return self._arr.pop(0)

    def removeTail(self):
        # удаление из хвоста
        if not self._arr:
            return None
        return self._arr.pop()  
    
    @property
    def isEmpty(self):
        return len(self._arr) == 0
        
    def size(self):
        return len(self._arr)
    
    def __str__(self):
        return str(self._arr)
    
    def __repr__(self):
        return str(self)
    
    def __getitem__(self, index):
        return self._arr[index]
        

def is_palindrom(s: str):
    if len(s) < 2:
        return True
    
    d = Deque()
    for c in s:
        d.addTail(c)
    
    while d[0] == d[-1]:
        d.removeFront()
        if d.isEmpty:
            return True        
        d.removeTail()
        if d.isEmpty:
            return True
        
    return False
