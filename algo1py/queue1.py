class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None

class LinkedList3:  
    def __init__(self):
        self.dummy = Node(None)
        
    @property
    def head(self):
        return self.dummy.next
    
    @property
    def tail(self):
        return self.dummy.prev
    
    def __str__(self):
        if self.isEmpty:
            return ""
        
        item = self.head
        ans = ""        
        
        while item != self.dummy:
            ans = ans + str(item.value) + " "
            item = item.next
        return ans
    
    @property 
    def isEmpty(self):
        return self.head == None and self.tail == None
    
    def insert(self, afterNode: Node, newNode: Node):
        if self.isEmpty:
            self.dummy.next = newNode
            self.dummy.prev = newNode
            newNode.prev = self.dummy
            newNode.next = self.dummy
            return
    
        if afterNode == None:
            afterNode = self.dummy
        
        newNode.prev = afterNode
        newNode.next = afterNode.next
        afterNode.next.prev = newNode
        afterNode.next = newNode

    def add_in_tail(self, newNode):
        self.insert(self.tail, newNode)
    
    def add_in_head(self, newNode):
        self.insert(None, newNode)
        
    def find(self, val):
        if self.isEmpty:
            return None
        node = self.head
        while node != self.dummy:
            if node.value == val:
                return node
            node = node.next
        return None

    def find_all(self, val):
        ans = []
        if self.isEmpty:
            return ans        
        
        node = self.head
        while node != self.dummy:
            if node.value == val:
                ans.append(node)
            node = node.next
        return ans        
    
    def delete_node(self, node):    
        if node is None or self.isEmpty:
            return        
         
        if self.dummy.next == node and self.dummy.prev == node:
            self.clean()
            return
        
        node.prev.next = node.next
        node.next.prev = node.prev    
 
    def delete_head(self):
        if self.isEmpty:
            return
        
        if self.head == self.tail:
            self.clean()
            return
        
        self.delete_node(self.head)
    
    def delete_tail(self):
        if self.isEmpty:
            return
        
        if self.head == self.tail:
            self.clean()
            return
        
        self.delete_node(self.tail)     
        

    def delete(self, val, all=False):
        if self.isEmpty:
            return
        
        if not all:
            self.delete_node(self.find(val))
            return
        
        node = self.head
        while node != self.dummy:
            nxt = node.next
            if node.value == val:
                self.delete_node(node)
            node = nxt

    def clean(self):
        self.dummy.prev = None
        self.dummy.next = None


    def __len__(self):
        if self.isEmpty:
            return 0
        node = self.head
        ans = 0
        while node != self.dummy:
            ans += 1
            node = node.next
        return ans # здесь будет ваш код

class Stack:
    def __init__(self):
        self.stack = LinkedList3()
        
    @property
    def isEmpty(self):    
        return self.stack.isEmpty
    
    def size(self):
        return len(self.stack)

    def pop(self):
        if self.stack.isEmpty:
            return None
        val = self.stack.head.value
        self.stack.delete_head()
        return val

    def push(self, value):
        self.stack.add_in_head(Node(value))

    def peek(self):
        if self.stack.isEmpty:
            return None # если стек пустой
        return self.stack.head.value
    
    def clean(self):
        self.stack.clean()
        
    def __str__(self):
        return str(self.stack)
    
    def __repr__(self):
        return str(self.stack)

class Queue:
    def __init__(self):
        self.leftStack = Stack()
        self.rightStack = Stack()

    def enqueue(self, item):
        self.leftStack.push(item)
    
    def dequeue(self):
        if self.rightStack.isEmpty:
            while not self.leftStack.isEmpty:
                self.rightStack.push(self.leftStack.pop())
        return self.rightStack.pop()        
        
    def size(self):
        return self.leftStack.size() + self.rightStack.size()
    
    def clean(self):
        self.leftStack.clean()
        self.rightStack.clean()
    
    @property
    def isEmpty(self):
        return self.leftStack.isEmpty and self.rightStack.isEmpty
    
    def __str__(self):
        ans = ""
        for s in str(self.leftStack).split():
            ans = s + ' ' + ans
        return  str(self.rightStack) + ans
    
    def __repr__(self):
        return str(self)
    
    def shift(self, N:int):
        if self.isEmpty:
            return
        for i in range(N):
            self.enqueue(self.dequeue())
            
            
            
