from generator_abst import *
import unittest

class test_abst(unittest.TestCase):
    def test_bstH(self):
        self.assertEqual(bstH(1),0)
        self.assertEqual(bstH(2),1)
        self.assertEqual(bstH(3),1)
        self.assertEqual(bstH(4),2)
        self.assertEqual(bstH(7),2)
        self.assertEqual(bstH(8),3)
        self.assertEqual(bstH(14),3)
        self.assertEqual(bstH(15),3)
        self.assertEqual(bstH(16),4)
        
    def test_generate(self):
        self.assertEqual(generatebbstarray([1, 2, 3]), [2, 1, 3])
        self.assertEqual(generatebbstarray(['a', 'f', 'h', 'm', 'p', 's', 'y']), ['m', 'f', 's', 'a', 'h', 'p', 'y'])
        self.assertEqual(generatebbstarray(['y', 'f', 'h', 'm', 'p', 'a', 's']), ['m', 'f', 's', 'a', 'h', 'p', 'y'])
        self.assertEqual(generatebbstarray(['a', 'b', 'c', 'f', 'g', 'h', 'k', 'm', 'p', 'q', 'r', 's', 'x', 'y', 'z']), \
                         ['m', 'f' ,'s', 'b', 'h', 'q', 'y', 'a', 'c', 'g' ,'k', 'p', 'r', 'x', 'z'])
        self.assertEqual(generatebbstarray(['a',  'x', 'f', 'g', 'h', 'k', 'm', 'z', 'p', 'q', 'b', 'c', 'r', 's',  'y']), \
                         ['m', 'f' ,'s', 'b', 'h', 'q', 'y', 'a', 'c', 'g' ,'k', 'p', 'r', 'x', 'z'])   
    
    def test_generate2(self):
        bst = generatebbstarray([50,25,75,20,37, 62,84,19,21,31, 43,55,70,80,92])        
        self.assertEqual(bst, [50,25,75,20,37, 62,84,19,21,31, 43,55,70,80,92])
        
if __name__ == "__main__":
    unittest.main()