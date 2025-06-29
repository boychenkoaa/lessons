'''
дерево проекта имеет ограничения на добавление:
к нодам определенных видов можно добавлять ноды только разрешенных (заранее оговоренных) других видов
этот функционал лучше вынести отдельно: "тип" ноды назовем NodeMark
в каждой из них будем хранить символьную "марку" ноды, список допустимых марок детей, и функционал проверки (является / не является)
'''

class TreeNode:
    def __init__(self, value):
        self._value = value
        self._children = []
        
    def add_child(self, node: TreeNode):
        self._children.append(node)

class NodeMark:
    mark: str = "_"
    children: str = ""
    
    def can_have_child(self, mark: str) -> bool:
        return mark in self.children
    
    def can_be_child(self, other: NodeMark):
        return other.has_child(self.mark)

class LayerNodeMark(NodeMark):
    mark: str = 'L'
    children: 'T'
    
class SliceNodeMark(NodeMark):
    mark: str = 'S'
    children: str = "L"
    
class SliceFamily(NodeMark):
    mark: str = 'F'
    children: str = "L"
    
class Trajectory(NodeMark):
    mark: str = 'T'
    children: str = ""
    
class ProjectEntity:
    ...

class TreeNodeMarked(TreeNode, NodeMark):
    def add_child(self, node: TreeNodeMarked):
        if self.can_have_child(node):
            super.add_child(node)
