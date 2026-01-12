class QueueNode:
    def __init__(self, val, prev, next):
        self.value = val
        self.next = next
        self.prev = prev
    
    def __str__(self):
        return str(self.value)
        
        
class Queue:
    def __init__(self):
        self._dummy = QueueNode(None, None, None)
        self._dummy.next = self._dummy
        self._dummy.prev = self._dummy
    
    @property
    def head(self):
        return self._dummy.next
    
    @property
    def tail(self):
        return self._dummy.prev
    
    @property
    def is_empty(self):
        return self._dummy.next == self._dummy
    
    def push(self, value):
        new_node = QueueNode(value, self._dummy, self.head)
        self.head.prev = new_node
        self._dummy.next = new_node
        return new_node
        
    def pop(self):
        ans = self.tail.value
        self._dummy.prev = self.tail.prev
        self._dummy.prev.next = self._dummy
        return ans
    
    def clear(self):
        self._dummy.prev = self._dummy
        self._dummy.next = self._dummy
        
    def size(self):
        node = self.head
        ans = 0
        while node != self._dummy:
            ans += 1
            node = node.next
        return ans
    
    def __str__(self):
        node = self.head
        ans = ""
        while node != self._dummy:
            ans += str(node) + " "
            node = node.next
        return ans

class BSTNode:

    def __init__(self, key, val, parent):
        self.NodeKey = key # ключ узла
        self.NodeValue = val # значение в узле
        self.Parent = parent # родитель или None для корня
        self.LeftChild = None # левый потомок
        self.RightChild = None # правый потомок
    
    def __str__(self):
        return str(self.NodeKey)
    
    def __repr__(self):
        return str(self)


class BSTFind: # промежуточный результат поиска
    def __init__(self):
        self.Node = None # None если 
        # в дереве вообще нету узлов

        self.NodeHasKey = False # True если узел найден
        self.ToLeft = False # True, если родительскому узлу надо 
        # добавить новый узел левым потомком
    
    def __str__(self):
        return str(self.Node)
    
    def __repr__(self):
        return str(self)

IN_ORDER = 0
POST_ORDER = 1
PRE_ORDER = 2

class BST:
    def __init__(self, node):
        self.Root = node # корень дерева, или None
    
    def compare_keys(self, key1, key2):
        return key1 < key2
    
    def FindNodeByKey(self, key):
        node = self.Root
        ans = BSTFind()
        while node != None:
            if node.NodeKey == key:
                ans.Node = node
                ans.NodeHasKey = True
                return ans
            
            ans.Node = node
            ans.ToLeft = self.compare_keys(key, node.NodeKey)
            if ans.ToLeft:
                node = node.LeftChild
            else:
                node = node.RightChild
            
        return ans # возвращает BSTFind

    def AddKeyValue(self, key, val):
        # добавляем ключ-значение в дерево
        bst_find = self.FindNodeByKey(key)
        if bst_find.NodeHasKey:
            return False
        if bst_find.Node == None:
            self.Root = BSTNode(key, val, None)
            return True
        
        parent_node = bst_find.Node
        new_node = BSTNode(key, val, parent_node)
        if bst_find.ToLeft:
            parent_node.LeftChild = new_node
        else:
            parent_node.RightChild = new_node
        return new_node
        

    def FinMinMax(self, FromNode, FindMax):
        # ищем максимальный/минимальный ключ в поддереве
        # возвращается объект типа BSTNode
        node = FromNode
        parent_node = None
        while node != None:
            parent_node = node
            if FindMax:
                node = node.RightChild
            else:
                node = node.LeftChild
                
        return parent_node
    
    # удаляет если лист или ровно 1 потомок
    # иначе возвращает False
    def delete_node_stupid(self, node_for_delete):
        has_left_child = (node_for_delete.LeftChild != None)
        has_right_child = (node_for_delete.RightChild != None)
        if has_left_child and has_right_child:
            return False
        
        is_root = (node_for_delete.Parent == None)
        is_left_for_parent = (not is_root) and (node_for_delete.Parent.LeftChild == node_for_delete)
        
        child = node_for_delete.RightChild
        if has_left_child:
            child = node_for_delete.LeftChild
        if child != None:
            child.Parent = node_for_delete.Parent
            
        if is_root:
            self.Root = child
        elif is_left_for_parent:
            node_for_delete.Parent.LeftChild = child
        else:
            node_for_delete.Parent.RightChild = child
        return True        
    
    def DeleteNodeByKey(self, key):
        # удаляем узел по ключу
        bst_find = self.FindNodeByKey(key)
        if not bst_find.NodeHasKey:
            return False # если узел не найден
        
        node_for_delete = bst_find.Node
        if not self.delete_node_stupid(node_for_delete):
            # оба ребенка на месте 
            # последователь (successor) точно не None
            successor = self.FinMinMax(node_for_delete.RightChild, FindMax=False)
            node_for_delete.NodeKey = successor.NodeKey
            node_for_delete.NodeValue = successor.NodeValue
            self.delete_node_stupid(successor)
        
        return True
        
    def _walk_base(self, order, node, action, result_list):
        if node == None:
            return
        if order == PRE_ORDER:
            action(node, result_list)
            self._walk_base(order, node.LeftChild, action, result_list)
            self._walk_base(order, node.RightChild, action, result_list)
        elif order == IN_ORDER:
            self._walk_base(order, node.LeftChild, action, result_list)
            action(node, result_list)
            self._walk_base(order, node.RightChild, action, result_list)
        elif order == POST_ORDER:
            self._walk_base(order, node.LeftChild, action, result_list)
            self._walk_base(order, node.RightChild, action, result_list)            
            action(node, result_list)
    
    def Count(self):
        def walk_count(node, result_list):
            result_list[0] += 1
        
        ans = [0]
        self._walk_base(PRE_ORDER, self.Root, walk_count, ans)
        return ans[0]
    
    def __str__(self):
        def walk_str(node, result_list):
            return result_list.append(str(node)) 
        
        str_list = []
        self._walk_base(PRE_ORDER, self.Root, walk_str, str_list)
        ans = ""
        for string in str_list:
            ans += string         
        return ans
    
    def DeepAllNodes(self, order):
        def append_node(node, result_list):
            return result_list.append(node) 
        
        nodes_list = []
        self._walk_base(order, self.Root, append_node, nodes_list)
        return tuple(nodes_list)
    
    def WideAllNodes(self):
        if self.Root == None:
            return tuple([])
        
        q = Queue()
        q.push(self.Root)
        ans = []
        while not q.is_empty:
            node = q.pop()
            if node.LeftChild != None:
                q.push(node.LeftChild)
            if node.RightChild != None:
                q.push(node.RightChild)
            ans.append(node)
        return tuple(ans)
        
    def __repr__(self):
        return str(self)

class BSTInversed(BST):
    def compare_keys(self, key1, key2):
        return key1 > key2
    
    def from_BST(self, bst: BST):
        all_nodes = bst.DeepAllNodes(PRE_ORDER)
        for node in all_nodes:
            self.AddKeyValue(node.NodeKey, node.NodeValue)
        
        
        
        