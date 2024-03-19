from heap import *
import unittest

class HeapTest(unittest.TestCase):
    def test_add(self):
        h = Heap()
        h.HeapArray = [-1] * 15
        h.Add(5)
        h.Add(6)
        h.Add(7)
        self.assertEqual(h.HeapArray, [7, 5, 6] + [-1]*12)
        
    def test_makeheap(self):
        h = Heap()
        h.MakeHeap([5, 6, 7], depth=4)
        self.assertEqual(h.HeapArray, [7, 5, 6] + [-1]*12)
        h.MakeHeap([3, 8, 6, 4, 5, 2], depth=4)
        self.assertEqual(h.HeapArray, [8, 5, 6, 3, 4, 2] + [-1]*9)
        
    def test_getmax(self):
        h = Heap()
        h.MakeHeap([3, 8, 6, 4, 5, 2], depth=4)
        h_sorted = [h.GetMax() for i in range(10)]
        self.assertEqual(h_sorted, [8, 6, 5, 4, 3, 2, -1, -1, -1, -1])
        
        
if __name__ == "__main__":
    unittest.main()
        
    