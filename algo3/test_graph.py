from graph import *
import unittest

class test_graph(unittest.TestCase):
    def test_add_vertex(self):
        g = SimpleGraph(5)
        g.AddVertex("a")
        g.AddVertex("b")
        self.assertEqual(g.vertex[0].Value, "a")
        self.assertEqual(g.vertex[1].Value, "b")
        self.assertEqual(g.m_adjacency[0][1], 0)
        self.assertEqual(g.m_adjacency[1][0], 0)
        
    def test_add_edge(self):
        g = SimpleGraph(5)
        g.AddVertex("a")
        g.AddVertex("b")        
        g.AddVertex("c")                      
        self.assertEqual(g.m_adjacency[0][2], 0)
        self.assertEqual(g.m_adjacency[2][0], 0)
        g.AddEdge(0, 2)
        self.assertEqual(g.m_adjacency[0][2], 1)
        self.assertEqual(g.m_adjacency[2][0], 1)
        
    def test_remove_edge(self):
        g = SimpleGraph(5)
        g.AddVertex("a")
        g.AddVertex("b")        
        g.AddVertex("c")                      
        self.assertEqual(g.m_adjacency[0][2], 0)
        g.AddEdge(0, 2)
        self.assertEqual(g.m_adjacency[0][2], 1)
        self.assertEqual(g.m_adjacency[2][0], 1)
        g.RemoveEdge(0, 2)
        self.assertEqual(g.m_adjacency[0][2], 0)
        self.assertEqual(g.m_adjacency[2][0], 0)

        
    def test_remove_vertex(self):
        g = SimpleGraph(5)
        g.AddVertex("a")
        g.AddVertex("b")        
        g.AddVertex("c")
        g.AddVertex("d")
        g.AddVertex("e")
        g.AddEdge(4, 1)
        g.AddEdge(2, 3)
        g.AddEdge(2, 4)
        g.AddEdge(2, 1)
        self.assertEqual(g.m_adjacency[1][4], 1)
        self.assertEqual(g.m_adjacency[2][3], 1)
        self.assertEqual(g.m_adjacency[2][4], 1)
        self.assertEqual(g.m_adjacency[1][2], 1)
        g.RemoveVertex(2)
        self.assertEqual(g.m_adjacency[1][4], 1)
        self.assertEqual(g.m_adjacency[2][3], 0)
        self.assertEqual(g.m_adjacency[2][4], 0)
        self.assertEqual(g.m_adjacency[1][2], 0)     
        
    def test_dfs(self):
        g = SimpleGraph(15)
        g.AddVertex("a")
        g.AddVertex("b")        
        g.AddVertex("c")
        g.AddVertex("d")
        g.AddVertex("e")
        g.AddVertex("f")
        g.AddVertex("g")
        g.AddVertex("h")
        g.AddVertex("j")
        g.AddEdge(1, 2)
        g.AddEdge(1, 3)
        g.AddEdge(1, 4)
        g.AddEdge(1, 5)
        g.AddEdge(5, 6)
        #g.AddEdge(2, 3)
        g.AddEdge(3, 4)
        g.AddEdge(4, 5)
        g.AddEdge(3, 8)
        g.AddEdge(4, 8)
        g.AddEdge(7, 8)
        way = g.DepthFirstSearch(8, 2)
        self.assertEqual(way, [8,3,1,2])
    

if __name__ == "__main__":
    unittest.main()

