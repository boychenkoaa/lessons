class ListNode:
    def __init__(self, value, prev, next):
        self.value = value
        self.prev = prev
        self.next = next
        
class List:
    def __init__(self):
        self._dummy = ListNode(None, None, None)
        self._dummy.next = self._dummy
        self._dummy.prev = self._dummy
    
    @property
    def is_empty(self):
        return self._head == self._dummy
    
    @property
    def _head(self):
        return self._dummy.next
    
    @property
    def _tail(self):
        return self._dummy.prev
    
    def insert_after_node(self, after_node:ListNode, value):
        new_node = ListNode(value, after_node, after_node.next)
        after_node.next.prev = new_node
        after_node.next = new_node
        
    def delete_node(self, node: ListNode):
        node.prev.next = node.next
        node.next.prev = node.prev
        return node.value
    
    def delete_head(self):
        if self.is_empty:
            return None
        return self.delete_node(self._dummy.next)
    
    def delete_tail(self):
        if self.is_empty:
            return None
        return self.delete_node(self._dummy.prev)    
    
    def insert_head(self, value):
        self.insert_after_node(self._dummy, value)
    
    def insert_tail(self, value):
        self.insert_after_node(self._dummy.prev, value)   
    
    @property
    def head_value(self):
        return self._head.value
    
    @property
    def tail_value(self):
        return self.tail.value    
        
    def clear(self):
        self._dummy.next = self._dummy
        self._dummy.prev = self._dummy
    
    @property
    def values_list(self):
        ans = []
        node = self._dummy.next
        while node != self._dummy:
            ans.append(node.value)
            node = node.next
        return ans
    
    def __str__(self):
        return str(self.values_list)
    
    def __repr__(self):
        return str(self)
    
class Stack:
    def __init__(self):
        self._li = List()
        
    def push(self, value):
        self._li.insert_head(value)
    
    def pop(self):
        return self._li.delete_head()
    
    def clear(self):
        self._li.clear()
    
    @property
    def values_list(self):
        return self._li.values_list
    
    @property
    def top(self):
        return self._li.head_value
    
    def __repr__(self):
        return str(self._li)    
    
class Queue:
    def __init__(self):
        self._li = List()
    
    @property
    def is_empty(self):
        return self._li.is_empty
        
    def push(self, value):
        self._li.insert_tail(value)
    
    def pop(self):
        return self._li.delete_head()
    
    def clear(self):
        self._li.clear()
    
    @property
    def values_list(self):
        return self._li.values_list
    
    @property
    def top(self):
        return self._li.head_value()
    
    def __repr__(self):
        return str(self._li)
    
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
    
    @property
    def vertices(self):
        return [v for v in range(self.max_vertex) if self.vertex[v] != None]
        

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
    
    def adjacency_list(self, v):
        if self.vertex[v] is None:
            return None
        return [i for i in range(self.max_vertex) if self.IsEdge(v, i)]
    
    def clear_hits(self):
        for v in self.vertex:
            if v != None:
                v.Hit = False        
    
    def DepthFirstSearch(self, VFrom, VTo):
        if VFrom == VTo:
            return [VFrom]
        
        self.clear_hits()
        
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
        
        vert_index_list = stack.values_list[::-1]
        ans = [self.vertex[v] for v in vert_index_list]
        return ans
    
    def _find_way_back_hits(self, v_from, v_to):
        stack = Stack()
        v = v_to
        stack.push(self.vertex[v])
        while v != v_from:
            v = self.vertex[v].Hit
            stack.push(self.vertex[v])
        return stack.values_list        
    
    def BreadthFirstSearch(self, VFrom, VTo):
        if VFrom == VTo:
            return [VFrom]
        
        self.clear_hits()      
        q = Queue()
        X = VFrom
        self.vertex[X].Hit = True
        q.push(X)
        while not q.is_empty:
            X = q.pop()
            for v in range(self.max_vertex):
                if self.m_adjacency[X][v] == 1 and self.vertex[v].Hit == False:
                    self.vertex[v].Hit = X
                    if v == VTo:
                        return self._find_way_back_hits(VFrom, VTo)
                    q.push(v)
                    
        return []
        
    
    def vertex_is_strong(self, v):
        adj_list = self.adjacency_list(v)
        return any(self.IsEdge(u, w) == 1 for u in adj_list for w in adj_list)
        
    def WeakVertices(self):
        # возвращает список узлов вне треугольников
        return [self.vertex[v] for v in self.vertices if not self.vertex_is_strong(v)]
                
    
        
    