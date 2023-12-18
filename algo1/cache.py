class NativeCache:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size
        self.hits = [0] * self.size
    
    def hash_fun(self, key):
        # в качестве key поступают строки!
        # всегда возвращает корректный индекс слота
        if key != "":
            return ord(key[0]) % self.size            
        return 0

    def is_key(self, key):
        # возвращает True если ключ имеется,
        # иначе False
        index = self.seek(key)
        return self.slots[index] == key

    
    # None если весь массив заполнен и такого элемента нет
    def seek(self, key):
        first_index = self.hash_fun(key)
        i = first_index
        while self.slots[i] != None and self.slots[i] != key:
            i = (i + 1) % self.size
            if i == first_index:
                return None
        return i
        
    def find_loser(self):
        min_hits = self.hits[0]
        min_index = 0
        for index in range(1, self.size):
            if self.hits[index] < min_hits:
                min_index = index
                min_hits = self.hits[index]
        return min_index
    
    # гарантированно записываем 
    # значение value по ключу key    
    def put(self, key, value):
        index = self.seek(key)
        if index == None:
            index = self.find_loser()
            self.hits[index] = 0
        self.slots[index] = key
        self.values[index] = value
        self.hits[index] += 1
        

    def get(self, key):
        # возвращает value для key, 
        # или None если ключ не найден
        index = self.seek(key)
        if index == None:
            return None
        self.hits[index] += 1
        return self.values[index]    
