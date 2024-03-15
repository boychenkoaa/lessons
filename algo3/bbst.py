class BSTNode:

    def __init__(self, key, parent):
        self.NodeKey = key # ключ узла
        self.Parent = parent # родитель или None для корня
        self.LeftChild = None # левый потомок
        self.RightChild = None # правый потомок
        self.Level = 0 # уровень узла
    
    @property 
    def is_leaf(self):
        return (self.LeftChild == None) and (self.RightChild == None)
        

class BalancedBST:
    def __init__(self):
        self.Root = None # корень дерева
        
    def _generate_from_sorted(self, parent: BSTNode, a_sorted: list, left_index: int, right_index: int, level: int):
        central_index = (right_index + left_index) // 2
        new_node = BSTNode(a_sorted[central_index], parent)
        new_node.Level = level
        if right_index > left_index:
            new_node.LeftChild = self._generate_from_sorted(new_node, a_sorted, left_index, central_index-1, level+1)
            new_node.RightChild = self._generate_from_sorted(new_node, a_sorted, central_index+1, right_index, level+1)
        return new_node
        
    def GenerateTree(self, a):
        a.sort()
        N = len(a)
        self.Root = self._generate_from_sorted(None, a, left_index=0, right_index=N-1, level=0)
    
    def _is_balanced_and_height(self, root_node: BSTNode):
        if root_node is None:
            return True , 0
        
        left_is_OK, left_height = self._is_balanced_and_height(root_node.LeftChild)
        right_is_OK, right_height = self._is_balanced_and_height(root_node.LeftChild)
        root_is_OK = left_is_OK and right_is_OK and abs(left_height - right_height) < 2
        height = max(left_height, right_height) + 1 
        return root_is_OK, height
        
    def IsBalanced(self, root_node):
        return self._is_balanced_and_height(root_node)[0]
        
    def _walk_preorder_str(self, node: BSTNode):
        if node is None:
            return ""
        return node.NodeKey + self._walk_preorder_str(node.LeftChild) + self._walk_preorder_str(node.RightChild)
    
    def __str__(self):
        return self._walk_preorder_str(self.Root)
    