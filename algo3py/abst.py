class aBST:
    def __init__(self, depth):
        # правильно рассчитайте размер массива для дерева глубины depth:
        tree_size = 2**(depth+1)-1
        self.Tree = [None] * tree_size # массив ключей

    def FindKeyIndex(self, key):
        # ищем в массиве индекс ключа
        index = 0
        while index <= len(self.Tree)-1:
            if self.Tree[index] is None:
                return -index
            if self.Tree[index] == key:
                return index
            if key < self.Tree[index]:
                index = index * 2 + 1
            else:
                index = index * 2 + 2
        return None # не найден

    def AddKey(self, key):
        index = self.FindKeyIndex(key)
        if index is None:
            return -1
        
        if index > 0:
            return index
        
        if index < 0 or index == 0 and self.Tree[0] is None:
            self.Tree[-index] = key
        return -index
                
        
        # индекс добавленного/существующего ключа или -1 если не удалось
