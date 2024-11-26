from __future__ import annotations
from math import sin, cos, atan
from functools import partial

Point2 = tuple[float, float]
Point3 = tuple[float, float, float]
Pline2_raw = list[Point2]
Arc2_raw = tuple[Point2, Point2, Point2]
Segment2_raw = tuple[Point2, Point2]
LinearGeom_raw = Pline2_raw | Arc2_raw | Segment2_raw
Vector = list[float]
Vector2_raw = Point2
Matrix2_raw = tuple[Vector2_raw, Vector2_raw]
Vector3_raw = tuple[Point3, Point3]
Matrix3_raw = tuple[Vector3_raw, Vector3_raw, Vector3_raw]

X, Y, Z = 0, 1, 2
EPSILON = 1e-4

def rot_matrix2(angle: float) -> Matrix2_raw:
    ...
    
def dot_mm2(m1: Matrix2_raw, m2: Matrix2_raw) -> Matrix2_raw:
    ...

def dot_mv2(m: Matrix2_raw, v: Vector2_raw) -> Vector2_raw:
    ...
    
def dot_vv2(v1: Vector2_raw, v2: Vector2_raw) -> float:
    ...
    
def sub(v1: Vector2_raw, v2: Vector2_raw):
    ...
    
def mul_kv(k: float, v: Vector2_raw):
    ...
    
def add(v1: Vector2_raw, v2: Vector2_raw):
    ...
    
def neg(v: Vector2_raw):
    ...
  
def angle (p1: Point2, p2: Point2, p3: Point2) -> float:
    ...

def distance_pp(p1: Point2, p2: Point2) -> float:
    ...

def predicate_left_rot(a: Point2, b: Point2, c: Point2) -> float:
    ...


def rot2_point(point: Point2, rot_center: Point2, angle: float) -> Point2:
    return Point2()

def rot2_linear_geom(linear_geom: LinearGeom_raw, rot_center: Point2, angle: float):
    rot2_carried = partial(rot2_point, rot_center=rot_center, angle=angle) 
    return tuple(map(rot2_carried, linear_geom))
