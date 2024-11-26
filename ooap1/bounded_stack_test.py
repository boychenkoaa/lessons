import unittest
from bounded_stack import * 

class Test_Bounded_Stack(unittest.TestCase):
    def test_size(self):
        stack = BoundedStack()
        self.assertEqual(stack.size, 0)
    
    def test_push(self):
        stack = BoundedStack(2)
        stack.push(5)
        stack.push(6)
        self.assertEqual(stack.size, 2)    
        self.assertEqual(str(stack), "6 5")    
        self.assertEqual(stack.push_status, stack.PUSH_OK)
        stack.push(7)
        self.assertEqual(stack.push_status, stack.PUSH_ERR)
        self.assertEqual(stack.size, 2)
        
        stack = BoundedStack(3)
        stack.push(5)
        stack.push(6)
        stack.push(7)
        self.assertEqual(stack.size, 3)
        self.assertEqual(str(stack), "7 6 5")    
    
    def test_pop(self):
        stack = BoundedStack()
        stack.push(5)
        stack.push(6)
        stack.push(7)
        stack.pop()
        self.assertEqual(stack.pop_status, stack.POP_OK)
        stack.pop()
        self.assertEqual(stack.pop_status, stack.POP_OK)
        stack.pop()
        self.assertEqual(stack.pop_status, stack.POP_OK)
        stack.pop()
        self.assertEqual(stack.pop_status, stack.POP_ERR)        
        
    def test_peek(self):
        stack = BoundedStack()
        stack.push(5)
        stack.push(6)
        stack.push(7)
        self.assertEqual(stack.peek, 7)
        self.assertEqual(stack.pop_status, stack.POP_NIL)
        self.assertEqual(stack.peek_status, stack.PEEK_OK)
        stack.pop()
        self.assertEqual(stack.peek, 6)
        self.assertEqual(stack.pop_status, stack.POP_OK)
        self.assertEqual(stack.peek_status, stack.PEEK_OK)
        stack.pop()
        self.assertEqual(stack.pop_status, stack.POP_OK)
        self.assertEqual(stack.peek, 5)
        self.assertEqual(stack.peek_status, stack.PEEK_OK)
        stack.pop()
        a = stack.peek
        self.assertEqual(stack.pop_status, stack.POP_OK)
        self.assertEqual(stack.peek_status, stack.PEEK_ERR)
    
    def test_clean(self):
        stack = BoundedStack()
        stack.push(5)
        stack.push(6)
        stack.push(7)
        stack.clear()
        self.assertEqual(stack.size, 0)


if __name__ == '__main__':
    unittest.main()
