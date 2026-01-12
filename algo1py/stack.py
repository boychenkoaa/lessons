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
    
    
def brackets(bracket_str: str):
    st = Stack()
    for c in bracket_str:
        if c == st.peek():
            st.push(c)
        else:
            st.pop()
    return st.stack.isEmpty


def rpn(s: str):
    def is_int_str(string: str):
        if len(string) == 0:
            return False
        return string.isdigit() or (len(string) >= 2 and string[0] == '-' and string[1:].isdigit())
    
    def bin_op(symbol, op2, op1):
        ans = None
        if symbol == '+':
            ans = op1 + op2
        elif symbol == '-':
            ans = op1 - op2
        elif symbol == '*':
            ans = op1 * op2
        elif (symbol == '/') and (op2 != 0):
            ans = op1 / op2
        return ans
            
    s1 = Stack()
    s2 = Stack()
    lexem_list = s.split()[::-1]
    for lexem in lexem_list:
        s1.push(lexem)
    
    while s1.size() > 0:
        elem = s1.pop()
        
        if elem == '=':
            return s2.pop()
        elif is_int_str(elem):
            s2.push(int(elem))
        else:
            result = bin_op(elem, s2.pop(), s2.pop())
            if result == None:
                raise ValueError('Incorrect lexem -> ' + str(elem))
            
            s2.push(result)
    return s2.pop()
            
            
          
                
        
