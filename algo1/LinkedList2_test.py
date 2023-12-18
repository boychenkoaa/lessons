from LinkedList2 import *

def test_init():
    li = LinkedList2()
    assert (li.head == None) and (li.tail==None)
    
def test_add_tail():
    li = LinkedList2()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    assert str(li) == "5 6 7 "
    print("add_tail ОК")
    

def test_add_head():
    li = LinkedList2()
    li.add_in_head(Node(5))
    li.add_in_head(Node(6))
    li.add_in_head(Node(7))
    assert str(li) == "7 6 5 "
    print("add_head ОК")
    
    
def test_find_val():
    li = LinkedList2()
    assert li.find(5) == None
    li.add_in_tail(Node(5))
    assert li.find(5) == li.head
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))
    assert li.find(5) == li.head
    assert li.find(6) == li.head.next
    assert li.find(7) == li.head.next.next
    li.add_in_tail(Node(8))
    assert li.find(8) == li.tail
    print("find_val ОК")

    
def test_delete_tail():
    li = LinkedList2()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))
    assert str(li) == "5 6 7 5 " and li.head.value == 5 and li.tail.value == 5
    li.delete_tail()
    assert str(li) == "5 6 7 " and li.head.value == 5 and li.tail.value == 7
    li.delete_tail()
    assert str(li) == "5 6 " and li.head.value == 5 and li.tail.value == 6
    li.delete_tail()
    assert str(li) == "5 " and li.head.value == 5 and li.tail.value == 5
    li.delete_tail()
    assert str(li) == "" and li.head == None and li.tail == None
    print("delete_tail OK")

def test_delete_head():
    li = LinkedList2()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))
    assert str(li) == "5 6 7 5 " and li.head.value == 5 and li.tail.value == 5
    li.delete_head()
    assert str(li) == "6 7 5 " and li.head.value == 6 and li.tail.value == 5
    li.delete_head()
    assert str(li) == "7 5 " and li.head.value == 7 and li.tail.value == 5
    li.delete_head()
    assert str(li) == "5 " and li.head.value == 5 and li.tail.value == 5
    li.delete_head()
    assert str(li) == "" and li.head == None and li.tail == None
    print("delete_head OK")

def test_delete_node():
    li = LinkedList2()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))
    assert str(li) == "5 6 7 5 " and li.head.value == 5 and li.tail.value == 5
    li.delete_node(li.head.next.next)
    assert str(li) == "5 6 5 " and li.head.value == 5 and li.tail.value == 5
    li.delete_node(li.tail)
    assert str(li) == "5 6 " and li.head.value == 5 and li.tail.value == 6
    li.delete_node(li.head)
    assert str(li) == "6 " and li.head.value == 6 and li.tail.value == 6
    li.delete_node(li.tail)
    assert str(li) == "" and li.head == None and li.tail == None
    print("delete_node OK")    
    

def test_delete():
    li = LinkedList2()
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))
    assert str(li) == "5 6 7 5 " and li.head.value == 5 and li.tail.value == 5
    li.delete(5)
    assert str(li) == "6 7 5 " and li.head.value == 6 and li.tail.value == 5
    li.delete(7)
    assert str(li) == "6 5 " and li.head.value == 6 and li.tail.value == 5
    li.delete(6)
    assert str(li) == "5 " and li.head.value == 5 and li.tail.value == 5
    li.delete(5)
    assert str(li) == "" and li.head == None and li.tail == None
    print("delete OK")

def test_delete_all():
    li = LinkedList2()
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
    print("delete_all OK")

    
def test_find_all():
    li = LinkedList2()
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
    print("find_all OK")
    
def test_len():
    li = LinkedList2()
    assert li.len() ==0
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(7))
    li.add_in_tail(Node(5))
    li.add_in_tail(Node(6))
    li.add_in_tail(Node(5))
    assert li.len() ==6
    li.delete(6, all=True)
    assert li.len() == 4
    li.clean()
    assert li.len() == 0
    print("test_len OK")
    

def test_insert():
    li = LinkedList2()
    li.insert(None, Node(1))
    li.insert(li.head, Node(2))
    li.insert(None, Node(3))
    li.insert(li.head.next, Node(4))
    li.insert(li.tail, Node(5))
    assert str(li) == "1 2 4 3 5 "
    print("test_insert OK")
    
def test_list_sum():
    li1 = LinkedList2()
    li1.add_in_tail(Node(1))
    li1.add_in_tail(Node(2))
    li1.add_in_tail(Node(3))
    li1.add_in_tail(Node(4))
    li1.add_in_tail(Node(5))
    li1.add_in_tail(Node(6))
    li2 = LinkedList2()
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
    print("test_list_sum OK")
    

test_init()
test_add_tail()
test_add_head()
test_find_val()
test_delete_tail()
test_delete_head()
test_delete_node()
test_delete()
test_delete_all()
test_find_all()
test_len()
test_insert()
# test_list_sum()
