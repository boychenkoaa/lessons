from abst import *
import unittest


class test_abst(unittest.TestCase):
    def test_find(self):
        bst = aBST(3)
        self.assertEqual(bst.FindKeyIndex("w"), 0)
        bst.Tree[0] = 'm'
        bst.Tree[1] = 'd'
        self.assertEqual(bst.FindKeyIndex("w"), -2)
        bst.Tree[2] = 'w'
        self.assertEqual(bst.FindKeyIndex("m"), 0)
        self.assertEqual(bst.FindKeyIndex("d"), 1)
        self.assertEqual(bst.FindKeyIndex("w"), 2)
        self.assertEqual(bst.FindKeyIndex("a"), -3)
        self.assertEqual(bst.FindKeyIndex("f"), -4)
        self.assertEqual(bst.FindKeyIndex("n"), -5)
        self.assertEqual(bst.FindKeyIndex("y"), -6)
        bst.Tree[3] = 'a'
        bst.Tree[4] = 'f'
        self.assertEqual(bst.FindKeyIndex("b"), None)
        bst.Tree[5] = 'n'
        bst.Tree[6] = 'y'
        self.assertEqual(bst.FindKeyIndex("b"), None)
        
    def test_add(self):
        bst = aBST(3)
        self.assertEqual(bst.AddKey("m"), 0)
        self.assertEqual(bst.AddKey("w"), 2)
        self.assertEqual(bst.AddKey("f"), 1)
        self.assertEqual(bst.AddKey("f"), 1)
        self.assertEqual(bst.AddKey("d"), 3)
        self.assertEqual(bst.AddKey("k"), 4)
        self.assertEqual(bst.AddKey("c"), -1)
        self.assertEqual(bst.AddKey("s"), 5)
        self.assertEqual(bst.AddKey("y"), 6)
        self.assertEqual(bst.AddKey("z"), -1)
        
if __name__ == "__main__":
    unittest.main()
