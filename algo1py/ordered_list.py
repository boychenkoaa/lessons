class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None

class OrderedList:
    def __init__(self, asc):
        self.head = None
        self.tail = None
        self.__ascending = asc
        
    @property
    def isEmpty(self):
        return self.head == None
    
    def compare(self, v1, v2):
        if v1 < v2:
            return -1
        if v1 > v2:
            return 1
        return 0

    def add(self, value):
        
        def add_head(newNode):
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
            
        def add_tail(newNode):
            self.tail.next = newNode
            newNode.prev = self.tail
            self.tail = newNode
        
        def add_body(afterNode, newNode):
            newNode.next = afterNode.next
            newNode.prev = afterNode
            afterNode.next.prev = newNode
            afterNode.next = newNode            
            
        newNode = Node(value)
        if self.isEmpty:
            self.head = newNode
            self.tail = newNode
            return
        
        control_compare_value = -1
        if self.__ascending:
            control_compare_value = 1
            
        afterNode = Node(None)
        afterNode.next = self.head
        afterNode.prev = None
        
        while afterNode.next != None and (self.compare(value, afterNode.next.value) == control_compare_value):
            afterNode = afterNode.next
            
        if afterNode.next == self.head: # ни разу не сработали
            add_head(newNode)
        elif afterNode == self.tail:
            add_tail(newNode) 
        else:
            add_body(afterNode, newNode)
    
    def find(self, val):
        node = self.head
        while node != None:
            if self.compare(node.value, val) == 0:
                return node
            node = node.next
        return None
    
    def __delele_node(self, node):
        if node == None or self.isEmpty:
            return
        
        if self.head == self.tail:
            if node == self.head:
                self.clean(asc = self.__ascending)
                return
            return
        
        if node == self.head:
            self.head = self.head.next
            self.head.prev = None
            return
        
        if node == self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
            return
        
        node.prev.next = node.next
        node.next.prev = node.prev
        
    
    def delete(self, val):
        self.__delele_node(self.find(val))

    def clean(self, asc):
        self.head = None
        self.tail = None
        self.__ascending = asc

    def len(self):
        ans = 0
        node = self.head
        while node != None:
            ans += 1
            node = node.next
        return ans

    def get_all(self):
        r = []
        node = self.head
        while node != None:
            r.append(node)
            node = node.next
        return r
    
    def values(self):
        r = []
        node = self.head
        while node != None:
            r.append(node.value)
            node = node.next
        return r    

class OrderedStringList(OrderedList):
    def __init__(self, asc):
        super(OrderedStringList, self).__init__(asc)

    def compare(self, v1, v2):
        return super().compare(v1.strip(), v2.strip())
