class NativeDictionary:
    # seek корректно работает только если ключи нельзя удалять
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size

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

    
    def seek(self, key):
        first_index = self.hash_fun(key)
        i = first_index
        while self.slots[i] != None and self.slots[i] != key:
            i = (i + 1) % self.size
            if i == first_index:
                return None
        return i
            
    def put(self, key, value):
        index = self.seek(key)
        if index == None:
            return None
        self.slots[index] = key
        self.values[index] = value
        # гарантированно записываем 
        # значение value по ключу key

    def get(self, key):
        # возвращает value для key, 
        # или None если ключ не найден
        index = self.seek(key)
        return self.values[index]