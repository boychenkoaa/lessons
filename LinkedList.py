class Node:

    def __init__(self, v):
        self.value = v
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
        else:
            self.tail.next = item
        self.tail = item
    
    def __str__(self):
        ans = ""
        node = self.head
        while node != None:
            ans += str(node.value) + " "
            node = node.next
        return ans
        
    def print_all_nodes(self):
        node = self.head
        while node != None:
            print(node.value, end=' ')
            node = node.next
        print('')
        
        
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

    def delete(self, val, all=False):
        if self.isEmpty:
            return
                    
        prehead = Node(None)
        prehead.next = self.head
        item = prehead
        while item.next != None:
            if item.next.value == val:
                item.next = item.next.next
                if not all:
                    break
            else:
                item = item.next
        
        self.head = prehead.next
        prehead = None # !!!
        self.tail = item
                
    def clean(self):
        self.head = None
        self.tail = None
        
    def len(self):
        ans = 0
        node = self.head
        while node != None:
            ans += 1
            node = node.next        
        return ans # здесь будет ваш код

    def insert(self, afterNode, newNode):
        if self.isEmpty:
            self.head = newNode
            self.tail = newNode
        # to head
        elif afterNode is None:
            newNode.next = self.head
            self.head = newNode
        # to tail
        elif afterNode.next is None:
            afterNode.next = newNode
            self.tail = newNode
            newNode.next = None
        else:
            newNode.next = afterNode.next
            afterNode.next = newNode
    
    @property        
    def isEmpty(self):
        return self.head is None

    
def list_sum(list1: LinkedList, list2: LinkedList):
    if list1.len() == list2.len():
        node1 = list1.head
        node2 = list2.head
        ans = LinkedList()
        while node1 != None:
            ans.add_in_tail(Node(node1.value + node2.value))
            node1 = node1.next
            node2 = node2.next
        return ans
    return None
