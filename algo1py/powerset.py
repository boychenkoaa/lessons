class PowerSet:

    def __init__(self):
        # ваша реализация хранилища
        self.storage = {}

    def size(self):
        return len(self.storage)
        # количество элементов в множестве

    def put(self, value):
        self.storage[value] = 1
        # всегда срабатывает

    def get(self, value):
        return self.storage.get(value) != None

    def remove(self, value):
        return self.storage.pop(value, None) != None
    
    def intersection(self, set2):
        ans = PowerSet()
        for key in self.storage.keys():
            if set2.get(key):
                ans.put(key)
        return ans

    def union(self, set2):
        ans = PowerSet()
        ans.storage.update(self.storage)
        ans.storage.update(set2.storage)
        return ans

    def difference(self, set2):
        ans = PowerSet()
        for key in self.storage.keys():
            if not set2.get(key):
                ans.put(key)
        return ans

    def issubset(self, set2):
        for key in set2.storage.keys():
            if not self.get(key):
                return False
        return True
