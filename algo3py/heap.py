class Heap:
    def __init__(self):
        self.HeapArray = [] # хранит неотрицательные числа-ключи
        self.size = 0
        
    def MakeHeap(self, a: list[int], depth: int):
        self.HeapArray = [-1] * (2 ** (depth + 1) - 1)
        self.size = 0
        # создаём массив кучи HeapArray из заданного
        # размер массива выбираем на основе глубины depth 
        for elem in a:
            self.Add(elem)
    
    def SiftDown(self):
        i = 0
        while i < len(self.HeapArray) // 2:
            swap_i = 2 * i + 1
            if self.HeapArray[2 * i + 2] > self.HeapArray[swap_i]:
                swap_i = 2 * i + 2
                
            if self.HeapArray[i] >= self.HeapArray[swap_i]:
                break
            
            self.HeapArray[i],  self.HeapArray[swap_i] = self.HeapArray[swap_i],  self.HeapArray[i]
            i = swap_i
        
    def SiftUp(self):
        i = self.size - 1
        while i > 0:
            swap_i = (i - 1) // 2
            if self.HeapArray[i] < self.HeapArray[swap_i]:
                break
            
            self.HeapArray[i],  self.HeapArray[swap_i] = self.HeapArray[swap_i],  self.HeapArray[i]
            i = swap_i
                
    def GetMax(self) -> int:
        if self.size == 0:
            return -1 # если куча пуста
        
        ans = self.HeapArray[0]
        self.HeapArray[0] = self.HeapArray[self.size-1]
        self.HeapArray[self.size-1] = -1
        self.size -= 1
        self.SiftDown()
        return ans

    def Add(self, key) -> bool:
        # если куча вся заполнена
        if self.size == len(self.HeapArray):
            return False
        
        self.HeapArray[self.size] = key
        self.size += 1
        self.SiftUp()
        return True
