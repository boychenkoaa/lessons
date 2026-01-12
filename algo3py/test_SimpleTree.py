from SimpleTree import *
import unittest

class test_simpletree(unittest.TestCase):
   def test_init(self):
      tree = SimpleTree(SimpleTreeNode(1, None))
      self.assertEqual(tree.Root.NodeValue, 1)
      self.assertEqual(tree.LeafCount(), 1)
      self.assertEqual(tree.Count(), 1)
   
   def test_addchild(self):
      tree = SimpleTree(SimpleTreeNode(1, None))
      self.assertEqual(tree.Count(), 1)
      
      node2 = SimpleTreeNode(2, None)
      tree.AddChild(tree.Root, node2)
      self.assertEqual(tree.Count(), 2)
      self.assertEqual(tree.Root.Children[0].NodeValue, 2)
      
      node3 = SimpleTreeNode(3, None)
      tree.AddChild(tree.Root, node3)
      self.assertEqual(tree.Count(), 3)
      self.assertEqual(tree.Root.Children[0].NodeValue, 2)
      self.assertEqual(tree.Root.Children[1].NodeValue, 3)
      
      node4 = SimpleTreeNode(4, None)
      tree.AddChild(tree.Root.Children[0], node4)
      self.assertEqual(tree.Root.Children[1].NodeValue, 3)
      self.assertEqual(tree.Count(), 4)
   
   def test_find(self):
      tree = SimpleTree(SimpleTreeNode(1, None))
      node2 = SimpleTreeNode(2, None)
      tree.AddChild(tree.Root, node2)
      node3 = SimpleTreeNode(3, None)
      tree.AddChild(tree.Root, node3)
      node4 = SimpleTreeNode(4, None)
      tree.AddChild(tree.Root.Children[0], node4)
      node5 = SimpleTreeNode(2, None)
      tree.AddChild(tree.Root.Children[1], node5)
      
      self.assertEqual(len(tree.FindNodesByValue(1)), 1)
      self.assertEqual(len(tree.FindNodesByValue(2)), 2)
      self.assertEqual(len(tree.FindNodesByValue(3)), 1)
      self.assertEqual(len(tree.FindNodesByValue(4)), 1)
      self.assertEqual(len(tree.FindNodesByValue(5)), 0)
   
   def test_move(self):
      tree = SimpleTree(SimpleTreeNode(1, None))
      node2 = SimpleTreeNode(2, None)
      tree.AddChild(tree.Root, node2)
      node3 = SimpleTreeNode(3, None)
      tree.AddChild(tree.Root, node3)
      node4 = SimpleTreeNode(4, None)
      tree.AddChild(tree.Root.Children[0], node4)
      node5 = SimpleTreeNode(5, None)
      tree.AddChild(tree.Root.Children[1], node5)
      node6 = SimpleTreeNode(6, None)
      tree.AddChild(tree.Root.Children[1], node6)
      
      self.assertEqual(tree.Root.Children[0].NodeValue, 2)
      self.assertEqual(tree.Root.Children[1].NodeValue, 3)
      
      tree.MoveNode(tree.Root.Children[0], tree.Root.Children[1])
      self.assertEqual(tree.Root.Children[0].NodeValue, 3)
      self.assertEqual(tree.Root.Children[0].Children[0].NodeValue, 5)
      self.assertEqual(tree.Root.Children[0].Children[1].NodeValue, 6)
      self.assertEqual(tree.Root.Children[0].Children[2].NodeValue, 2)
      self.assertEqual(tree.Root.Children[0].Children[2].Children[0].NodeValue, 4)
      
   def test_count(self):
      tree = SimpleTree(SimpleTreeNode(1, None))
      self.assertEqual(tree.LeafCount(), 1)
      node2 = SimpleTreeNode(2, None)
      tree.AddChild(tree.Root, node2)
      node3 = SimpleTreeNode(3, None)
      tree.AddChild(tree.Root, node3)
      node4 = SimpleTreeNode(4, None)
      tree.AddChild(tree.Root.Children[0], node4)
      node5 = SimpleTreeNode(5, None)
      tree.AddChild(tree.Root.Children[1], node5)
      node6 = SimpleTreeNode(6, None)
      tree.AddChild(tree.Root.Children[1], node6)
      self.assertEqual(tree.LeafCount(), 3)
      self.assertEqual(tree.Count(), 6)
                       
      tree.MoveNode(tree.Root.Children[0], tree.Root.Children[1])
      self.assertEqual(tree.LeafCount(), 3)
      self.assertEqual(tree.Count(), 6)
      
        
if __name__ == "__main__":
    unittest.main()
