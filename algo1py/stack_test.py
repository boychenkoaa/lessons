import unittest
from stack import *

class Test_Stack(unittest.TestCase):
    def test_size(self):
        stack = Stack()
        self.assertEqual(stack.size(), 0)
    
    def test_push(self):
        stack = Stack()
        stack.push(5)
        stack.push(6)
        stack.push(7)
        self.assertEqual(stack.size(), 3)    
        self.assertEqual(str(stack), "7 6 5 ")    
    
    def test_pop(self):
        stack = Stack()
        stack.push(5)
        stack.push(6)
        stack.push(7)
        self.assertEqual(stack.pop(), 7)
        self.assertEqual(stack.pop(), 6)
        self.assertEqual(stack.pop(), 5)
        
    def test_peak(self):
        stack = Stack()
        stack.push(5)
        stack.push(6)
        stack.push(7)
        self.assertEqual(stack.peek(), 7)
        stack.pop()
        self.assertEqual(stack.peek(), 6)
        stack.pop()
        self.assertEqual(stack.peek(), 5)        
    
    
    def test_clean(self):
        stack = Stack()
        stack.push(5)
        stack.push(6)
        stack.push(7)
        stack.clean()
        self.assertEqual(stack.size(), 0)
        
    def test_brackets(self):
        self.assertEqual(brackets("(())"), True)
        self.assertEqual(brackets(""), True)
        self.assertEqual(brackets("((()))"), True)
        self.assertEqual(brackets("(()())"), True)
        self.assertEqual(brackets("(()()"), True)
        self.assertEqual(brackets("(()))"), True)
        
    def test_rpn(self):
        self.assertEqual(rpn("1 2 / 4 +"), 4.5)
        self.assertEqual(rpn("8 2 + 5 * 9 +"), 59)
        

if __name__ == '__main__':
    unittest.main()
