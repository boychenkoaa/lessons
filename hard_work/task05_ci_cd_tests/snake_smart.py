from geom2d_base import *
from bisect import bisect_left, insort, bisect
from enum import Enum
from copy import copy, deepcopy
from dataclasses import dataclass

@dataclass
class CombSegmentIntersection:
    start_index: int
    pline: Pline2

class Comb:
    def __init__(self, distances: list[float], angle: float, start_point: Point2):
        self.from_distances_angle(distances, angle, start_point)
    
    @property
    def distances_acc(self):
        return copy(self._distances_acc)
    
    @property
    def lines(self):
        return copy(self._lines)
    
    def _accumulate_distances(self, distances: list[float]):
        self._distances_acc = [distances[0]] + [None] * (len(distances) - 1)
        for i, d in enumerate(distances[1:], 1):
            self._distances_acc[i] = self._distances_acc[i-1] + d
    
    
    def from_distances_angle(self, distances: list[float], angle: float, start_point: Point2):
        self._accumulate_distances(distances)
        v = cos(angle), sin(angle)
        v_p = -sin(angle), cos(angle)
        self._start_line = Line2(p = start_point, v =v)
        self._lines = list(map(lambda d: move_line(self.start_line, mul(v_p, d)), self.distances_acc))
    
    @property
    def start_line(self):
        return self._start_line
    
    def bisect_point(self, point: Point2) -> int:
        d =  signed_dist_point_line2(point, self.start_line)[1]
        return bisect(self.distances_acc, d)
        
    def slice_segment(self, seg: Segment2) -> CombSegmentIntersection:
        index_b = self.bisect_point(seg.p)
        end =  add(seg.p, seg.v)
        index_e = self.bisect_point(end)
        if index_b > index_e:
            index_e, index_b = index_b, index_e
        
        # нет пересечения
        if index_b == len(self.lines) or index_e == 0:
            return CombSegmentIntersection(0, [])
        
        ans = CombSegmentIntersection(index_b, [ls2_intersect(line, seg) for line in self.lines[index_b:index_e]])
        return ans
        
@dataclass
class RasterPoint:
    point: Point2
    segment_index: int
    contour_index: int

RasterSegment = tuple[RasterPoint, RasterPoint]

# бусины
# точки растра, нанизанные на прямую
# можно сортировать вдоль прямой
# 
@dataclass
class Beads:
    line: Line2
    raster_points: list[RasterPoint] 
    is_sorted: bool
    
    def sort_points(self):
        self.raster_points.sort(key = lambda rp: t_by_point2(self.line, rp.point))
        self.is_sorted = True
        
    def add_raster_point(self, new_rp: RasterPoint):
        rp_proj = RasterPoint(contour_index = new_rp.contour_index, segment_index = new_rp.segment_index, \
                              point = projection_line2_point2(self.line, new_rp.point))
        self.raster_points.append(rp_proj)
        self.is_sorted = False
    
class Raster:
    def __init__(self):
        self._segments = []
        self._is_dash_line = False
        
    @property
    def is_dash_line(self):
        return self._is_dash_line
    
    @property
    def segments(self):
        return copy(self._segments)
    
    def from_beads(self, beads: Beads):
        self._is_dash_line = True
        beads.sort_points()
        self._segments = list(zip(beads.raster_points[::2], beads.raster_points[1::2]))
        
    def __len__(self):
        return len(self._segments)
        
    def pline(self) -> Pline2:
        return reduce(lambda x, y: x + y, self._segments)
        
    def add_segment(self, rs: RasterSegment):
        self._segments.append(rs)
        self._is_dash_line = False

class RasterLists:
    def __init__(self):
        self._rasters = []
    
    def add_dash_line(self, raster_dash_line: Raster):
        if len(self._rasters) == 0 or len(raster_dash_line) != len(self._rasters[-1]):
            self._rasters.append([])
        for a in raster_dash_line:
            self._rasters[-1].append(Raster())
        for raster,seg in zip(self._rasters[-1], raster_dash_line.segments):
            raster.add_segment(seg) 
        
    
    def get_raster(self, raster_line_index: int, raster_index: int):
        ...
        
    def all_rasters(self) -> list[Raster]:
        ...
        
    def __len__(self) -> int:
        ...
        

def snakes_of_polygon(polygon: Polygon2, distances, angle: float):
    ...
