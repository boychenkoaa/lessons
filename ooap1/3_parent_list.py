from typing import TypeVar, Iterable, Generic
from enum import Enum
T = TypeVar("T")

# самодеятельность, для краткости
class Status(Enum):
    NIL = 0
    ERR = 1
    OK = 2

class ParentListNode(Generic[T]):
    def __init__(self, prev_node: ParentListNode, next_node: ParentListNode, value: T, is_dummy: bool = False):
        self.prev = prev_node
        self.next = next_node
        self._value = value
        self._is_dummy = is_dummy
    
    @property
    def is_dummy(self):
        return self._is_dummy
    
    @property
    def value(self) -> T:
        return self._value


class ParentList (Generic[T]):
    def __init__(self):
        self.clear()
    
    def _set_nil_statuses(self):
        self._get_status = Status.NIL
        self._head_status = Status.NIL
        self._tail_status = Status.NIL
        self._right_status = Status.NIL
        self._put_right_status = Status.NIL
        self._put_left_status = Status.NIL
        self._remove_status = Status.NIL
        self._add_to_empty_status = Status.NIL
        self._add_tail_status = Status.NIL
        self._replace_status = Status.NIL
        self._find_status = Status.NIL
        self._replace_all_status = Status.NIL
        self._is_head_status =  Status.NIL
        self._is_tail_status =  Status.NIL
        self._remove_all_status == Status.NIL
    
    @property
    def _head_node(self):
        return self._dummy.next
    
    @property
    def _tail_node(self):
        return self._dummy.prev
    
    def _insert_after_node(self, node: ParentListNode, value):
        new_node = ParentListNode(node, node.next, value)
        node.next.prev = new_node
        node.next = new_node
        
    # запросы-статусы
    @property
    def get_status(self)  -> Status:
        return self._get_status
    
    @property
    def head_status(self)  -> Status:
        return self._head_status
    
    @property
    def tail_status(self) -> Status:
        return self._tail_status
    
    @property
    def right_status(self) -> Status:
        return self._right_status
    
    @property
    def put_right_status(self) -> Status:
        return self._put_right_status
    
    @property
    def put_left_status(self) -> Status:
        return self._put_left_status
    
    @property
    def remove_status(self) -> Status:
        return self._remove_status
    
    @property
    def add_to_empty_status(self) -> Status:
        return self._add_to_empty_status
    
    @property
    def add_tail_status(self) -> Status:
        return self._add_tail_status
    
    @property
    def replace_status(self) -> Status:
        return self._replace_status
    
    @property
    def find_status(self) -> Status:
        return self._find_status
    
    @property
    def replace_all_status(self) -> Status:
        return self._replace_all_status

    # запросы обычные
    # получить текущий элемент
    # предусловие: список не пуст
    def get(self) -> T:
        if not self.is_value:
            self._get_status == Status.ERR
            return None
        self._get_status == Status.OK
        return self._cursor.value
        
    # размер списка
    def size(self) -> int:
        return self._size
        
    # предусловие: список не пуст 
    @property
    def is_head(self) -> bool:
        if not self.is_value:
            self._is_head_status = Status.ERR
            return False
        return self._cursor == self._head_node
        
    # запрос -- в хвосте ли курсор
    # предусловие: список не пуст
    @property
    def is_tail(self) -> bool:
        if not self.is_value:
            self._is_tail_status = Status.ERR
            return False
        self._is_tail_status = Status.OK
        return self._cursor == self._tail_node
    
    # запрос -- пустой ли список
    @property
    def is_value(self) -> bool:
        return not self._dummy.next.is_dummy
    
    # команды
    # команда установить курсор в голову
    # предусловие -- список не пуст
    # постусловие -- курсор в голове
    def head(self):
        if not self.is_value:
            self._head_status = Status.ERR
            return
        self._cursor = self._head_node
        self._head_status = Status.OK
    
    # команда установить курсор в хвост
    # предусловие -- список не пуст
    # постусловие -- курсор в хвосте
    def tail(self):
        if not self.is_value:
            self._tail_status = Status.ERR
            return
        self._cursor = self._tail_node
        self._tail_status = Status.OK
    
    # команда курсор на 1 вправо
    # предусловие: список не пуст и курсор не в хвосте
    def right(self):
        if not self.is_value or self.is_tail:
            self._right_status = Status.ERR
            return
        self._cursor = self._cursor.next
        self._right_status = Status.OK
        
    # добавить элемент справа от курсора
    # предусловие -- список не пуст
    # постусловие -- добавлен 1 элемент
    def put_right(self, new_value):
        if not self.is_value:
            self._put_right_status = Status.ERR
            return
        
        new_node = ParentListNode(self._cursor, self._cursor.next, new_value)
        self._cursor.next.prev = new_node
        self._cursor.next = new_node
        self._size += 1
        self._put_right_status = Status.OK
        
    # добавить элемент слева от курсора
    # предусловие: список не пуст
    # постусловие: добавлен 1 элемент
    def put_left(self, new_value):
        if not self.is_value:
            self._put_left_status = Status.ERR
            return
        
        new_node = ParentListNode(self._cursor.prev, self._cursor, new_value)
        self._cursor.prev.next = new_node
        self._cursor.prev = new_node
        self._size += 1
        # не очень ясно, что делатm с постусловием
        # считать размер долго, проверять, что size увеличился на 1 нет смысла
        self._put_left_status = Status.OK        

    # удалить элемент под курсором и сдвинуть вправо по возможности (влево если нет возможности)
    # предусловие: список не пуст
    # постусловие: удален 1 элемент
    def remove(self):
        if not self.is_value:
            self._remove_status = Status.ERR
            return        
        self._cursor.next.prev = self._cursor.prev
        self._cursor.prev.next = self._cursor.next
        self._cursor = self._cursor.prev if self.is_tail else self._cursor.next
        self._size -= 1
        self._remove_status = Status.OK
        
    # очистка
    # постусловие: список пуст
    def clear(self):
        self._dummy = ParentListNode(None, None, None, is_dummy = True)
        self._dummy.next = self._dummy
        self._dummy.prev = self._dummy
        self._cursor = self._dummy
        self._size = 0
        self._set_nil_statuses()
    
    # команда - добавление в пустой список
    # предусловие: список пуст
    # постусловие: значиние курсора = new_value и размер = 1
    def add_to_empty(self, value):
        if self.is_value:
            self._add_to_empty_status = Status.ERR
            return
        self._insert_after_node(self._dummy, value)
        self._cursor = self._dummy.next
        
    № команда - добавление в хвост непустого списка
    # предусловие: список не пуст
    # постусловие: добавлен 1 элемент
    def add_tail(self, new_value: T):
        self._insert_after_node(self._tail_node)
    
    # команда -- установить по курсору значение new_value
    # предусловие: список не пуст
    # постусловие: текущее значение = new_value
    def replace(self, new_value: T):
        if not self.is_value:
            self._replace_status = Status.ERR
            return
        
        self._cursor.value = new_value
        self._replace_status = Status.OK
    
    # команда - установить курсор на первое вхождение new_value
    # предусловие: список не пуст и такое значение существует
    # постусловие: текущее значение = new_value
    def find(self, value: T):
        if not self.is_value:
            self._find_status = Status.ERR
            return 
        
        self._cursor = self._cursor.next
        while not (self._cursor.is_dummy or self._cursor.value == value):
            self._cursor = self._cursor.next
            
        self._find_status = Status.ERR if self._cursor.is_dummy else Status.OK
            
    # команда -- удалить все вхождения value        
    # предусловие -- список не пуст
    # постусловие: в спискне нет значений типа value (проверка неэффективна)
    def remove_all(self, value: T):
        if not self.is_value:
            self._remove_all_status == Status.ERR
            return
        
        self.find(value)
        while self.find_status == Status.OK:
            self.remove()
            self.find(value)
        
        self._remove_all_status = Status.OK
        

LinkedList = ParentList

class TwoWayList(ParentList):
    def _set_nil_statuses(self):
        super()._set_nil_statuses()
        self._left_status = Status.NIL
        
    # команда -- сдвинуть курсор влево, если возможно
    # предусловие -- курсор не в голове и список не пуст
    def left(self):
        if not self.is_value or self.is_tail:
            self._left_status = Status.ERR
            return
        self._cursor = self._cursor.prev
        self._left_status = Status.OK
    
    # запрос статуса сдвига влево
    @property
    def left_status(self):
        return self._left_status
