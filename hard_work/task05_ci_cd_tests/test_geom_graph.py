from unittest import TestCase, main
from geomgraph import * 

class TestGeomGraph(TestCase):
    def test_dim(self):
        gg = GeomGraph(0.0001, 2)
        self.assertEqual(gg.dim, 2)
        
    def test_find_point(self):
        gg = GeomGraph(0.0001, 2)
        id1 = gg.add_vertex((1, 2))
        id2 = gg.add_vertex((3, 4.0000001))
        id3 = gg.find_point((3, 4))
        self.assertNotEqual(id3, None)
        id4 = gg.find_point((3, 4.01))
        self.assertEqual(id4, None)
        
    def test_add(self):
        gg = GeomGraph(0.0001, 2)
        id1 = gg.add_vertex((1, 2))
        id2 = gg.add_vertex((3, 4.0000001))
        id3 = gg.add_vertex((3, 4))
        id4 = gg.add_vertex((3, 4.01))
        self.assertEqual(id2, id3)
        self.assertNotEqual(id3, id4)
        
        
    def test_add_edge(self):
        gg = GeomGraph(0.0001, 2)
        id1 = gg.add_vertex((1, 2))
        id2 = gg.add_vertex((3, 4.0000001))
        id3 = gg.add_vertex((3, 4))
        id4 = gg.add_vertex((3, 4.01))        
        gg.add_edge(id1, id2, 0)
        self.assertEqual(gg.degree(id1), 1)
        self.assertEqual(gg.degree(id2), 1)
    
    def test_degree(self):
        gg = GeomGraph(0.01, 2)
        id0 = gg.add_vertex((0, 0))
        id1 = gg.add_vertex((1, 0))
        id2 = gg.add_vertex((1, 1))
        id3 = gg.add_vertex((0, 1))
        self.assertEqual(gg.degree(id0), 0)
        self.assertEqual(gg.degree(id1), 0)
        self.assertEqual(gg.degree(id2), 0)
        self.assertEqual(gg.degree(id3), 0)
        gg.add_edge(id0, id1, 0)
        gg.add_edge(id2, id3, 0)
        self.assertEqual(gg.degree(id0), 1)
        self.assertEqual(gg.degree(id1), 1)
        self.assertEqual(gg.degree(id2), 1)
        self.assertEqual(gg.degree(id3), 1)
        gg.add_edge(id1, id2, 0)
        self.assertEqual(gg.degree(id0), 1)
        self.assertEqual(gg.degree(id1), 2)
        self.assertEqual(gg.degree(id2), 2)
        self.assertEqual(gg.degree(id3), 1)        
        
    def test_connectivity_components(self):
        gg = GeomGraph(0.01, 2)
        self.assertEqual(len(gg.connectivity_components), 0)
        id0 = gg.add_vertex((0, 0))
        id1 = gg.add_vertex((1, 0))
        id2 = gg.add_vertex((1, 1))
        id3 = gg.add_vertex((0, 1))
        self.assertEqual(len(gg.connectivity_components), 4)
        gg.add_edge(id0, id1, 0)
        gg.add_edge(id2, id3, 0)        
        self.assertEqual(len(gg.connectivity_components), 2)
        gg.add_edge(id1, id2, 0)
        self.assertEqual(len(gg.connectivity_components), 1)
    
    def test_recognize_gg(self):
        gg = GeomGraph(0.01, 2)
        self.assertEqual(recognize_connected_gg(gg), ggConnectedTopology.EMPTY)
        id0 = gg.add_vertex((0, 0))
        self.assertEqual(recognize_connected_gg(gg), ggConnectedTopology.POINT)
        id1 = gg.add_vertex((1, 0))
        id2 = gg.add_vertex((1, 1))
        id3 = gg.add_vertex((0, 1))
        gg.add_edge(id0, id1, 0)
        gg.add_edge(id2, id3, 0)
        gg.add_edge(id1, id2, 0)
        self.assertEqual(recognize_connected_gg(gg), ggConnectedTopology.PLINE)
        gg.add_edge(id3, id0, 0)
        self.assertEqual(recognize_connected_gg(gg), ggConnectedTopology.CONTOUR)

if __name__ == "__main__":
    main()