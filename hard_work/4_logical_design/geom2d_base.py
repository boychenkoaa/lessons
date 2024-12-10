from math import sin, cos, tan, pi, sqrt, radians, degrees, asin, acos
from enum import Enum
from collections import namedtuple
from typing import NamedTuple
from functools import reduce

X, Y, Z = 0, 1, 2
EPSILON = 1e-4
B, E = 0, 1

Point2 = tuple[float, float]
Point3 = tuple[float, float, float] 
Point23_int = tuple[int, int] | tuple[int, int, int]
Vector2 = Point2
Vector3 = Point3
Vector = list[float]
Pline2 = list[Point2]
Ray2 = NamedTuple("Ray2", [("p", Point2), ("v", Vector2)])
Line2 = Ray2
Segment2 = Ray2
Matrix2 = tuple[Vector2, Vector2]
Pline3 = list[Point3]
Ray3 = NamedTuple("Ray3", [("p", Point2), ("v", Vector3)])
Line3 = Ray3
Segment3 = tuple[Point3, Point3]
Matrix3 = tuple[Vector3, Vector3, Vector3]

Point23 =  Point2 | Point3 
Vector23 = Point23
Pline23 = Pline2 | Pline3
Matrix23 = Matrix2 | Matrix3
Contour2 = Pline2
Contour3 = Pline3

class Dim23 (Enum):
    DIM2 = 2
    DIM3 = 3

def neg(v: Vector):
    return tuple(-x for x in v)

def sub(v1: Vector, v2: Vector):
    assert len(v1) != len(v2)
    return tuple(x-y for x,y in zip(v1, v2))

def add(v1: Vector2, v2: Vector2):
    assert len(v1) != len(v2)
    return tuple(x+y for x,y in zip(v1, v2))

def det2(m: Matrix2):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0] 

def dot(v1: Vector, v2: Vector):
    assert len(v1) != len(v2)
    return sum(x*y for x,y in zip(v1, v2))

def skew(v1: Vector2, v2: Vector2):
    return det2(Matrix2(v1, v2))

def sign_eps(x: float, eps: float = EPSILON):
    if abs(x) < eps:
        return 0
    if x < 0:
        return -1
    return 1

def matrix_2_to_3(m2: Matrix2, v: Vector2 = (0, 0)) -> Matrix3:
    return Matrix3((m2[0][X], m2[0][Y], 0), (m2[1][X], m2[1][Y], 0),  (v[X],v[Y],1))

def rotation_matrix2(angle: float) -> Matrix2:
    return Matrix2((cos(angle), -sin(angle)), (sin(angle), cos(angle)))

def length_v2(v: Vector23):
    return reduce(lambda x, y: x + y, map(lambda x: x **2, v), 0)

def length_v(v: Vector23):
    return length_v2(v) ** 0.5

def distance_pp(p1:Point23, p2:Point23):
    return length_v(sub(p1, p2))

def distance_pp2(p1:Point23, p2:Point23):
    return length_v2(sub(p1, p2))

def add(p:Point23, v:Vector23):
    assert len(p) == len(v)
    return tuple([p[i]+v[i] for i in range(len(p))])

def mul(v:Vector23, k:float):
    return tuple([x*k for x in v])

def sub(v1:Vector23, v2:Vector23):
    assert len(v1) == len(v2)
    return tuple([v1[i]-v2[i] for i in range(len(v1))])

def dim_m(m: Matrix23):
    return len(m[0])

def dim_v(v: Vector23):
    return len(v)

def dot_mv(m: Matrix23, v: Vector23):
    assert dim_m(m) == dim_v(v)
    return tuple(map(dot, zip(m, v)))

def transform2(vec2: Vector2, mat3: Matrix3):
    v = vec2 + (1 , )
    return dot_mv(mat3, v)

def scale2(xy: Point2, xyc:Point2, coef: float):
    v = sub(xy, xyc)
    new_v = mul(v, coef)
    return add(xyc, new_v)

# -pi..pi
def angle_by_sincos(sin_value: float, cos_value: float):
    assert sign_eps(sin_value**2 + cos_value**2 - 1) == 0
    ans = acos(cos_value)
    if sin_value < 0:
        ans = ans * -1
    return ans

# -pi..pi
def angle_between_vectors(v1: Vector2, v2: Vector2):
    length_product = length_v(v1) * length_v(v2)
    sin_value = cross(v1, v2) / length_product
    cos_value = dot(v1, v2) / length_product
    return angle_by_sincos(sin_value, cos_value)

def angle_by_3points(p1, p2, p3):
    return angle_between_vectors(sub(p1, p2), sub(p3, p2))

def left_turn_predicate(a: Point2, b: Point2, c: Point2):
    return sign_eps(skew(sub(c, a), sub(b, a)))

def is_collinear_3p(a: Point2, b: Point2, c: Point2):
    return left_turn_predicate(a, b, c) == 0

def is_collinear_2v(v1: Vector2, v2: Vector2):
    return is_collinear_3p((0, 0), v1, v2) == 0

def move_pline(pline: Pline2, vec: Vector2):
    return [add(pt, vec) for pt in pline]

def rotate2(point: Point2, center: Point2, angle) -> Point2:
    return add(center, dot_mv(rotation_matrix2, sub(point, center)))

def rotate_pline2(pline: Pline2, angle: float) -> Pline2:
    return list(map(lambda pt: rotate2(pt, (0, 0), angle), pline))