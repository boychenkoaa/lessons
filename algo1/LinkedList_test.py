
from LinkedList import *

def test_init():
    li = LinkedList()
    assert (li.head == None) and (li.tail==None)
    
def test_add_tail():
    li = LinkedList()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    assert str(li) == "5 6 7 "
    
def test_find_val():
    li = LinkedList()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))
    assert li.find(5) == li.head
    assert li.find(6) != None
    assert li.find(7) != None
    li.add_in_tail(Node(8))
    assert li.find(8) == li.tail

def test_find_val_empty():
    li = LinkedList()
    assert li.find(5) == None
    
def test_delete_once():
    li = LinkedList()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))    
    li.delete(5, all=False)
    assert str(li) == "6 7 5 " and li.head.value == 6 and li.tail.value == 5
    li.delete(6)
    assert str(li) == "7 5 " and li.head.value == 7 and li.tail.value == 5
    li.delete(7, all=False)
    assert str(li) == "5 " and li.head.value == 5 and li.tail.value == 5
    li.delete(5, all=False)
    assert str(li) == "" and li.head == None and li.tail == None
    
def test_delete_all():
    li = LinkedList()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))    
    li.delete(5, all=True)
    assert str(li) == "6 7 " and li.head.value == 6 and li.tail.value == 7
    li.delete(6)
    assert str(li) == "7 " and li.head.value == 7 and li.tail.value == 7
    li.delete(7, all=True)
    assert str(li) == "" and li.head == None and li.tail == None

def test_delete_all2():
    li = LinkedList()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(5))    
    li.delete(5, all=True)
    assert str(li) == "" and li.head == None and li.tail == None
    
def test_find_all():
    li = LinkedList()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(5))
    assert (len(li.find_all(5)) == 3)
    assert (len(li.find_all(6)) == 2)
    assert (len(li.find_all(7)) == 1)
    assert (len(li.find_all(8)) == 0)

def test_len():
    li = LinkedList()
    assert li.len() ==0
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(5))
    assert li.len() ==6
    li.delete(6, all=True)
    assert li.len() ==4
    li.clean()
    assert li.len() ==0
    

def test_insert():
    li = LinkedList()
    li.insert(None, Node(1))
    li.insert(li.head, Node(2))
    li.insert(None, Node(3))
    li.insert(li.head.next, Node(4))
    li.insert(li.tail, Node(5))
    assert str(li) == "3 1 4 2 5 "
    
def test_list_sum():
    li1 = LinkedList()
    li1.add_in_tail(Node(1))
    li1.add_in_tail(Node(2))
    li1.add_in_tail(Node(3))
    li1.add_in_tail(Node(4))
    li1.add_in_tail(Node(5))
    li1.add_in_tail(Node(6))
    li2 = LinkedList()
    li2.add_in_tail(Node(1))
    li2.add_in_tail(Node(2))
    li2.add_in_tail(Node(3))
    li2.add_in_tail(Node(4))
    li2.add_in_tail(Node(5))
    li2.add_in_tail(Node(6))    
    li_sum = list_sum(li1, li2)
    assert str(li_sum) == "2 4 6 8 10 12 "
    
    li2.delete(1)
    li_sum = list_sum(li1, li2)
    assert li_sum == None
    
    li1.clean()
    li2.clean()
    li_sum = list_sum(li1, li2)
    assert li_sum.isEmpty
    
    

test_init()
test_add_tail()
test_find_val()
test_find_val_empty()
test_delete_once()
test_delete_all()
test_delete_all2()
test_find_all()
test_len()
test_insert()
test_list_sum()
