class HashTable:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size

    def hash_fun(self, value):
        if value == "":
            return 0
        ans = ord (value[-1]) % self.size
        return ans

    def seek_slot(self, value):
        # находит индекс пустого слота для значения, или None
        index = self.hash_fun(value)
        first_index = index
        while self.slots[index] != None and self.slots[index] != value:
            index = (index + self.step) % self.size
            if index == first_index:
                return None
        return index

    def put(self, value):
        index = self.seek_slot(value)
        if index != None:
            self.slots[index] = value
        return None

    def find(self, value):
        index = self.hash_fun(value)
        first_index = index
        while self.slots[index] != value:
            index = (index + self.step) % self.size
            if index == first_index:
                return None        
        return index
    