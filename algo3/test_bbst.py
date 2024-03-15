from bbst import *
import unittest

class test_simpletree(unittest.TestCase):
    def test_generate (self):
        bst = BalancedBST()
        bst.GenerateTree(['o', 'b', 'a', 's', 'c', 'w', 'y'])
        self.assertEqual(str(bst), "obacwsy")
        
    def test_is_balanced(self):
        bst = BalancedBST()
        bst.GenerateTree(['o', 'b', 'a', 's', 'c', 'w', 'y'])        
        self.assertEqual(bst.IsBalanced(bst.Root), True)
        
        
        
  
                       



if __name__ == "__main__":
    unittest.main()
