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
    
    def GetAllNodes(self):
        def Walk(children, all_nodes_list):
            all_nodes_list.extend(children)
            for child in children:
                Walk(child.Children, all_nodes_list)
        
        if self.Root == None:
            return []
        ans = []
        children = [self.Root]
        Walk(children, ans)
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
