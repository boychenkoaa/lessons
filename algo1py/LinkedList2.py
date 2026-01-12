class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None

class LinkedList2:  
    def __init__(self):
        self.head = None
        self.tail = None

        
    def __str__(self):
        item = self.head
        ans = ""
        while item != None:
            ans = ans + str(item.value) + " "
            item = item.next
        return ans
    
    @property 
    def isEmpty(self):
        return self.head == None
    
    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
            item.prev = None
            item.next = None
        else:
            self.tail.next = item
            item.prev = self.tail
        self.tail = item

    def find(self, val):
        node = self.head
        while node != None:
            if node.value == val:
                return node
            node = node.next
        return None

    def find_all(self, val):
        ans = []
        node = self.head
        while node != None:
            if node.value == val:
                ans.append(node)
            node = node.next
        return ans        
    
    def delete_head(self):
        if self.isEmpty:
            return
        
        if self.head == self.tail:
            self.clean()
            return
        
        self.head = self.head.next
        self.head.prev = None
    
    def delete_tail(self):
        if self.isEmpty:
            return
        
        if self.head == self.tail:
            self.clean()
            return
        
        self.tail = self.tail.prev
        self.tail.next = None            
        
    
    def delete_node(self, node):
        if node is None:
            return        
        
        if node == self.head:
            self.delete_head()
            return
        
        if node == self.tail:
            self.delete_tail()
            return
        
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def delete(self, val, all=False):
        if self.isEmpty:
            return
        
        if not all:
            self.delete_node(self.find(val))
            return
        
        node = self.head
        while node != None:
            nxt = node.next
            if node.value == val:
                self.delete_node(node)
            node = nxt

    def clean(self):
        self.head = None
        self.tail = None

    def len(self):
        node = self.head
        ans = 0
        while node != None:
            ans += 1
            node = node.next
        return ans # здесь будет ваш код

    def insert(self, afterNode, newNode):
        if afterNode is None or afterNode == self.tail:
            self.add_in_tail(newNode)
            return
        
        newNode.prev = afterNode
        newNode.next = afterNode.next
        afterNode.next.prev = newNode
        afterNode.next = newNode
        
    def add_in_head(self, newNode):
        if self.head is None:
            self.tail = newNode
        else:
            newNode.next = self.head
            newNode.prev = None
            self.head.prev = newNode
        self.head = newNode
