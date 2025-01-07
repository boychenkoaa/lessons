from __future__ import annotations
from geom2d_base import * 
from graph import *
from points1 import *
from copy import deepcopy


Edge = tuple[int, int]

class GeomGraph:
    def __init__(self, epsilon: float, dim: Dim23):
        self._points = StrangePoints(epsilon, dim)
        self._graph = BiGraph()
    
    @property
    def epsilon(self) -> float:
        return self._points.epsilon
    
    @property
    def dim(self) -> Dim23:
        return self._points.dim
    
    @property
    def graph(self):
        return deepcopy(self._graph)
    
    def degree(self, id_: int):
        return self.graph.degree(id_)
        
    @property
    def dim(self):
        return self._points.dim
    
    def find_point(self, point: Point23) -> int|None:
        return self._points.ext(point)
    
    def add_vertex(self, point: Point23):
        id_ = self.find_point(point)
        if id_ is None:
            id_ = self._graph.add_vertex(point)
            self._points.add(point, id_)
        return id_
    
    def add_edge(self, id_from: int, id_to: int, edge_value):
        self._graph.update_edge(id_from, id_to, edge_value)
    
    @property
    def all_vertices(self) -> list[Point23Ext]:
        return [Point23Ext(point=self._graph[id_], ext=id_) for id_ in self._graph.verts]
    
    @property
    def all_edges(self) -> list(Edge):
        return self._graph.edges
    
    def remove(self, id_):
        point = self._graph[id_]
        self._graph.pop_vertex(id_)
        self._points.remove(point)
    
    def reject(self, id_set: set[int]):
        self._graph.reject(id_set)
        self._points = StrangePoints(self.epsilon, self.dim)
        for id_ in self._graph.verts:
            self._points.add(self._graph[id_])
            
    def subgraph(self, id_set) -> GeomGraph:
        ans = deepcopy(self)
        ans.reject(id_set)
        return ans
    
    @property
    def connectivity_components(self):
        return list(map(self.subgraph, connectivity_components(self._graph)))
    
    @property
    def is_connected(self) -> bool:
        return len(self.connectivity_components) == 1
    
    def __getitem__(self, item: int) -> Point23:
        return self._graph[int]
        
 
class ggConnectedTopology (Enum):
    UNKNOWN = -1
    EMPTY = 0
    POINT = 1
    SEGMENT = 2
    PLINE = 3
    CONTOUR = 4

ggTopology = list[ggConnectedTopology]
    
def recognize_connected_gg(gg_connected: GeomGraph) -> ggConnectedTopology:
    Nverts = len(gg_connected.all_vertices)
    degrees = [gg_connected.degree(vert.ext) for vert in gg_connected.all_vertices]
    count2 = degrees.count(2)    
    count1 = degrees.count(1)
    
    if Nverts == 0:
        return ggConnectedTopology.EMPTY
    
    if Nverts == 1:
        return ggConnectedTopology.POINT
    
    if Nverts == 2:
        return ggConnectedTopology.SEGMENT
    
    if count2 == Nverts:
        return ggConnectedTopology.CONTOUR
    
    if count1 == 2 and count2 == Nverts - 2:
        return ggConnectedTopology.PLINE
    
    return ggConnectedTopology.UNKNOWN