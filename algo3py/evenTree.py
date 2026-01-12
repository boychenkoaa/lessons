class StackNode:
    def __init__(self, val, next):
        self.value = val
        self.next = next
        
class Stack:
    def __init__(self):
        self._dummy = StackNode(None, None)
        
    @property 
    def head(self):    
        return self._dummy.next
    
    @property 
    def is_empty(self):
        return self.head == None
    
    def push(self, new_value):
        self._dummy.next = StackNode(new_value, self._dummy.next)
        
    def pop(self):
        if self.is_empty:
            return None
        
        ans = self.head.value
        self._dummy.next = self.head.next
        return ans
    
    def clear(self):
        self._dummy.next = None
        
class SimpleTreeNode:
    def __init__(self, val, parent):
        self.NodeValue = val # значение в узле
        self.Parent = parent # родитель или None для корня
        self.Children = [] # список дочерних узлов

class SimpleTree:
    def __init__(self, root):
        self.Root = root # корень, может быть None

    def AddChild(self, ParentNode, NewChild):
        if ParentNode == None:
            self.Root = NewChild
        else:
            ParentNode.Children.append(NewChild)
            NewChild.Parent = ParentNode

    def DeleteNode(self, NodeToDelete):
        parent = NodeToDelete.Parent
        if parent is None:
            self.Root = None
        else:
            parent.Children.remove(NodeToDelete)
    
    def WalkPreOrder(self, node: SimpleTreeNode, action):
        if node == None:
            return
        action(node)
        for child in node.Children:
            self.WalkPreOrder(child, action)
    
    def WalkPostOrder(self, node: SimpleTreeNode, action):
        if node == None:
            return
        
        for child in node.Children:
            self.WalkPostOrder(child, action)
        action(node)
    
    def GetAllNodes(self):
        def walk_action(node):
            ans.append(node)
        
        ans = []
        self.WalkPreOrder(self.Root, walk_action)
        return ans

    def FindNodesByValue(self, val):
        return list(filter(lambda node: node.NodeValue == val, self.GetAllNodes()))

    def MoveNode(self, OriginalNode, NewParent):
        self.DeleteNode(OriginalNode)
        self.AddChild(NewParent, OriginalNode)

    def Count(self):
        return len(self.GetAllNodes())

    def LeafCount(self):
        return len(list(filter(lambda node: len(node.Children)==0, self.GetAllNodes())))
    
    def EvenTrees(self):
        def walk_action(node:SimpleTreeNode):
            is_even = False
            for child in node.Children:
                is_even = (is_even == even_stack.pop())
            if is_even:
                ans.append(node.Parent)
                ans.append(node)
            even_stack.push(is_even)
       
        even_stack = Stack()
        ans = []
        self.WalkPostOrder(self.Root, walk_action)
        if len(ans)>=2 and ans[-2] == None:
            ans = ans[0:len(ans)-2]
        return ans
    
    def __str__(self):
        return str([node.NodeValue for node in self.GetAllNodes()])
