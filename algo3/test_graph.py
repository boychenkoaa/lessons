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
        way_values = [v.Value for v in way]
        self.assertEqual(way_values, ["j","d","b","c"])
        way = g.DepthFirstSearch(8, 6)
        way_values = [v.Value for v in way]
        self.assertEqual(way_values, ["j","d","b","e","f","g"])        
        
    def test_bfs(self):
        g = SimpleGraph(15)
        for c in "abcdefghjk":
            g.AddVertex(c)
        
        edges_list = [(1, 2), (1, 3), (1, 4), (1, 5), (5, 6), (3, 4), (4, 5), (3, 8), (4, 7), (4, 8), (7, 8)]  
        for edge in edges_list:
            g.AddEdge(*edge)
        
        way = g.BreadthFirstSearch(8, 6)
        way_values = [v.Value for v in way]
        self.assertEqual(way_values,["j","e","f","g"])    
        way = g.BreadthFirstSearch(9, 6)
        way_values = [v.Value for v in way]
        self.assertEqual(way_values,[])    
        way = g.BreadthFirstSearch(2, 7)
        way_values = [v.Value for v in way]
        self.assertEqual(way_values,["c", "b", "e", "h"])
        
    def test_weak(self):
        g = SimpleGraph(15)
        for c in "abcdefghjk":
            g.AddVertex(c)
        edges_list = [(1, 6), (1, 7), (1, 8), (2, 3), (2, 4), (2, 5), (3, 5), (3, 6), (3, 7), (6, 8), (8, 9)]
        for edge in edges_list:
            g.AddEdge(*edge)
        
        self.assertEqual(g.WeakVertices(), [1, 2, 3, 5, 6, 8])
        
        g2 = SimpleGraph(15)
        for c in "abcde":
            g2.AddVertex(c)
        edges_list = [(1, 2), (2, 3), (3, 4), (4, 1)]
        for edge in edges_list:
            g2.AddEdge(*edge)        
        self.assertEqual(g2.WeakVertices(), [])
        
        g2.AddEdge(1, 3)
        self.assertEqual(g2.WeakVertices(), [1, 2, 3, 4])
        
        
if __name__ == "__main__":
    unittest.main()

