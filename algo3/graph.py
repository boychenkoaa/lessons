class StackNode:
    def __init__(self, val, next):
        self.value = val
        self.next = next
        
class Stack:
    def __init__(self):
        self._dummy = StackNode(None, None)
    
    @property
    def top(self):
        if self.head != None:
            return self.head.value
        return None
    
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
        
        ans = self.top
        self._dummy.next = self.head.next
        return ans
    
    def clear_to_list(self):
        ans = []
        while not self.is_empty:
            ans.append(self.pop())
        return ans
    
    def __repr__(self):
        ans = ""
        node = self.head
        while node != None:
            ans += str(node.value) + ' '
            node = node.next
        return ans
    
    def clear(self):
        self._dummy.next = None

class Vertex:
    def __init__(self, val):
        self.Value = val
        self.Hit = False

class SimpleGraph:

    def __init__(self, size):
        self.max_vertex = size
        self.m_adjacency = [[0] * size for _ in range(size)]
        self.vertex = [None] * size
        
    def AddVertex(self, v):
        for i in range(self.max_vertex):
            if self.vertex[i] == None:
                self.vertex[i] = Vertex(v)
                return i
        return None
            
        
    # здесь и далее, параметры v -- индекс вершины
    # в списке  vertex
    def RemoveVertex(self, v):
        # ваш код удаления вершины со всеми её рёбрами
        self.vertex[v] = None
        for i in range(self.max_vertex):
            self.m_adjacency[i][v] = 0
            self.m_adjacency[v][i] = 0
        

    def IsEdge(self, v1, v2):
        return self.m_adjacency[v1][v2] == 1 and self.m_adjacency[v2][v1] == 1
        
    def AddEdge(self, v1, v2):
        # добавление ребра между вершинами v1 и v2
        self.m_adjacency[v1][v2] = 1
        self.m_adjacency[v2][v1] = 1

    def RemoveEdge(self, v1, v2):
        # удаление ребра между вершинами v1 и v2
        self.m_adjacency[v1][v2] = 0
        self.m_adjacency[v2][v1] = 0
    
    def find_connected_nonvisited_vetrex(self, v):
        for i in range(self.max_vertex):
            if self.IsEdge(v, i) and not self.vertex[i].Hit:
                return i
        return None
    
    def DepthFirstSearch(self, VFrom, VTo):
        if VFrom == VTo:
            return [VFrom]
        
        for v in self.vertex:
            if v != None:
                v.Hit = False
        
        X = VFrom
        stack = Stack()
        stack.push(X)
        self.vertex[X].Hit = True
        while X != None:
            if self.m_adjacency[X][VTo] == 1:
                stack.push(VTo)
                break
            
            X = self.find_connected_nonvisited_vetrex(X)
            if X is None:
                stack.pop()
                X = stack.top
            else:
                stack.push(X)
                self.vertex[X].Hit = True
                
        return stack.clear_to_list()[::-1]