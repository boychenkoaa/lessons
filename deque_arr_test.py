from deque_arr import *
import unittest


class TestDeque(unittest.TestCase):
    def test_addFront(self):
        d = Deque()
        self.assertEqual(d.size(), 0)
        self.assertEqual(str(d), "[]")
        d.addFront(1)
        self.assertEqual(d.size(), 1)
        self.assertEqual(str(d), "[1]")
        d.addFront(2)
        self.assertEqual(d.size(), 2)
        self.assertEqual(str(d), "[2, 1]")
        d.addFront(3)
        self.assertEqual(d.size(), 3)
        self.assertEqual(str(d), "[3, 2, 1]")
        
    
    def test_addTail(self):
        d = Deque()
        self.assertEqual(d.size(), 0)
        self.assertEqual(str(d), "[]")
        d.addTail(1)
        self.assertEqual(d.size(), 1)
        self.assertEqual(str(d), "[1]")
        d.addTail(2)
        self.assertEqual(d.size(), 2)
        self.assertEqual(str(d), "[1, 2]")
        d.addTail(3)
        self.assertEqual(d.size(), 3)
        self.assertEqual(str(d), "[1, 2, 3]")
        d.addTail(4)
        self.assertEqual(d.size(), 4)
        self.assertEqual(str(d), "[1, 2, 3, 4]")        
    
 
    def test_removeFront(self):  
        d = Deque()
        d.addFront(1)
        d.addTail(2)
        d.addFront(3)
        d.addTail(4)
        self.assertEqual(str(d), "[3, 1, 2, 4]")
        self.assertEqual(d.size(), 4)
        self.assertEqual(d.removeFront(), 3)
        self.assertEqual(d.size(), 3)
        self.assertEqual(str(d), "[1, 2, 4]")
        self.assertEqual(d.removeFront(), 1)
        self.assertEqual(d.size(), 2)
        self.assertEqual(str(d), "[2, 4]")        
        self.assertEqual(d.removeFront(), 2)
        self.assertEqual(d.size(), 1)
        self.assertEqual(str(d), "[4]")                
        self.assertEqual(d.removeFront(), 4)
        self.assertEqual(d.size(), 0)
        self.assertEqual(str(d), "[]")        
        
    
    def test_removeTail(self):
        d = Deque()
        d.addFront(1)
        d.addTail(2)
        d.addFront(3)
        d.addTail(4)
        self.assertEqual(str(d), "[3, 1, 2, 4]")
        self.assertEqual(d.size(), 4)
        self.assertEqual(d.removeTail(), 4)
        self.assertEqual(d.size(), 3)
        self.assertEqual(str(d), "[3, 1, 2]")
        self.assertEqual(d.removeTail(), 2)
        self.assertEqual(d.size(), 2)
        self.assertEqual(str(d), "[3, 1]")        
        self.assertEqual(d.removeTail(), 1)
        self.assertEqual(d.size(), 1)
        self.assertEqual(str(d), "[3]")                
        self.assertEqual(d.removeTail(), 3)
        self.assertEqual(d.size(), 0)
        self.assertEqual(str(d), "[]")           
        
    
    def test_palindrom(self):    
        self.assertTrue(is_palindrom(""))
        self.assertTrue(is_palindrom("a"))
        self.assertTrue(is_palindrom("aa"))
        self.assertTrue(is_palindrom("aba"))
        self.assertTrue(is_palindrom("abba"))
        self.assertTrue(is_palindrom("abdba"))
        self.assertTrue(is_palindrom("abddba"))
        self.assertFalse(is_palindrom("ab"))
        self.assertFalse(is_palindrom("abb"))
        self.assertFalse(is_palindrom("abdb"))
        self.assertFalse(is_palindrom("abdaa"))
        self.assertFalse(is_palindrom("abddaa"))
        
    
if __name__ == '__main__':
    unittest.main()

     