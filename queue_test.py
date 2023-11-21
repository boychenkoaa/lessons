from queue1 import *
import unittest


class TestQueue(unittest.TestCase):
    def test_enqueue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(str(q), "1 2 3 ")
    
    def test_size(self):
        q = Queue()
        self.assertEqual(q.size(), 0)
        q.enqueue(1)
        self.assertEqual(q.size(), 1)
        q.enqueue(2)
        self.assertEqual(q.size(), 2)
        q.enqueue(3)
        self.assertEqual(q.size(), 3)

    def test_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual (q.dequeue(), 1)
        self.assertEqual (q.dequeue(), 2)
        self.assertEqual (q.dequeue(), 3)
        q.enqueue(4)
        q.enqueue(5)
        q.enqueue(6)
        q.enqueue(7)
        self.assertEqual (q.dequeue(), 4)
        self.assertEqual (q.dequeue(), 5)
        self.assertEqual (str(q), "6 7 ")
        self.assertEqual (q.dequeue(), 6)
        self.assertEqual (q.dequeue(), 7)        
        self.assertEqual (str(q), "")
        self.assertEqual (q.size(), 0)
        
    def test_all(self):  
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        q.dequeue()
        self.assertEqual (str(q), "2 3 ")
        q.enqueue(4)
        self.assertEqual (str(q), "2 3 4 ")
        
    def test_shift(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        q.enqueue(4)
        q.enqueue(5)
        q.enqueue(6)
        q.enqueue(7)
        self.assertEqual (str(q), "1 2 3 4 5 6 7 ")
        q.shift(2)
        self.assertEqual (str(q), "3 4 5 6 7 1 2 ")
        q.shift(2)
        self.assertEqual (str(q), "5 6 7 1 2 3 4 ")
        q.shift(3)
        self.assertEqual (str(q), "1 2 3 4 5 6 7 ")
    #
    
if __name__ == '__main__':
    unittest.main()

     