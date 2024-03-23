from evenTree import *
import unittest

class test_eventree(unittest.TestCase):
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

        
    def test_even(self):
        tree = SimpleTree(None)
        values = [node.NodeValue for node in tree.EvenTree()]
        self.assertEqual(values, [])        
        
        tree = SimpleTree(None)
        nodes = [SimpleTreeNode(i, None) for i in range(13)]
        tree.Root = nodes[1]
        tree.AddChild(tree.Root, nodes[2])
        tree.AddChild(tree.Root, nodes[3])
        tree.AddChild(tree.Root, nodes[6])
        tree.AddChild(nodes[2], nodes[5])
        tree.AddChild(nodes[2], nodes[7])
        tree.AddChild(nodes[3], nodes[4])
        tree.AddChild(nodes[6], nodes[8])
        tree.AddChild(nodes[8], nodes[9])
        tree.AddChild(nodes[8], nodes[10])
        values = [node.NodeValue for node in tree.EvenTree()]
        self.assertEqual(values, [1,3,1,6])
        tree.AddChild(nodes[5], nodes[11])
        tree.AddChild(nodes[7], nodes[12])
        values = [node.NodeValue for node in tree.EvenTree()]
        print(values)
        self.assertEqual(values, [2,5,2,7,1,3,1,6])
        
if __name__ == "__main__":
    unittest.main()
