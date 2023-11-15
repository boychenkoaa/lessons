from dyn import * 
import unittest

class TestDynArray(unittest.TestCase):
    def test_append(self):
        d =  DynArray()
        for i in range(16):
            d.append(i)
        
        self.assertEqual(d.capacity, 16)
        self.assertEqual(d.count, 16)
        d.append(16)
        self.assertEqual(d.capacity, 32)
        self.assertEqual(d.count, 17)
        
    def test_insert(self):
        d =  DynArray()
        d.insert(0, 0)
        d.insert(0, 1)
        d.insert(0, 2)
        d.insert(2, 3)
        d.insert(2, 4)
        d.insert(5, 5)
            
        self.assertEqual(d.capacity, 16)
        self.assertEqual(d.count, 6)

    def test_indexerror(self):
        d =  DynArray()
        d.insert(0, 0)
        d.insert(0, 1)
        d.insert(0, 2)
        d.insert(2, 3)
        d.insert(2, 4)
        d.insert(5, 5)
        with self.assertRaises(IndexError):
            d.insert(-1, 0)
        with self.assertRaises(IndexError):
            d.delete(-1)
        with self.assertRaises(IndexError):
            d.delete(15)        
        
    def test_delete(self):
        d =  DynArray()
        for i in range(17):
            d.append(i)
            
        self.assertEqual(d.capacity, 32)
        self.assertEqual(d.count, 17)    
        d.delete(0)
        self.assertEqual(d.capacity, 32)
        self.assertEqual(d.count, 16)
        d.delete(1)
        self.assertEqual(d.capacity, 21)
        self.assertEqual(d.count, 15)
        d.delete(1)
        self.assertEqual(d.capacity, 21)
        self.assertEqual(d.count, 14)
            

if __name__ == "__main__":
    unittest.main()