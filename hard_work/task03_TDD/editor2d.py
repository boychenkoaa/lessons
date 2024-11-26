from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from geom_raw import * 

DrawingObject = GeomLinear | wPoint2

class wPointStyle(Enum):
    UNKNOWN = 0
    DOT = 1
    PLUS = 2
    X = 3
    SQUARE = 4
    TRIANGLE = 5
    CIRCLE = 6
    ASTERISK = 7
    STRIKE_SQUARE = 8
    PLUS_BOLD = 9

@dataclass
class wPoint2:
    xy: Point2
    style: wPointStyle 

class CommandStatus(Enum):
    OK = "OK"
    FAIL = "FAIL"
    NEVER_CALLED = "NEVER_CALLED"
    
class ConverterCommandStatus(Enum):
    UNKNOWN_TYPE = "UNKNOWN_TYPE" 

# интерфейс
class GeomLinear:
    def __init__(self):
        self._last_status = CommandStatus.NEVER_CALLED
        
    @property
    def raw(self):
        ...
    
    @property    
    def length(self):
        ...
        
    @property
    def begin(self) -> Point2:
        ...
    
    @property
    def end(self) -> Point2:
        ...    
    
    @property
    def last_status(self) -> CommandStatus:
        return self._last_status
    
    def moveB(self, new_B: Point2):
        ...
        
    def moveE(self, new_E: Point2):
        ...    
    
    @property
    def reversed(self) -> GeomLinear:
        ...
        
    def transform(self, mat3: Matrix3_raw) -> GeomLinear:
        ...

class Segment2(GeomLinear):
    def __init__(self, begin: Point2, end: Point2):
        self._begin = begin
        self._end = end
    
    @property
    def begin(self) -> Point2:
        return self._begin
        
    @property
    def end(self) -> Point2:
        return self._end
        
    @property
    def reversed(self) -> GeomLinear:
        return Segment2(self.end, self.begin)
        
    def moveB(self, new_B: Point2):
        self._begin = new_B
        
    def moveE(self, new_E: Point2):
        self._end = new_E    

    def transform(self, mat3: Matrix3_raw) -> GeomLinear:
        ...
    
    
Vector2 = Point2

class Arc2(GeomLinear):
    def __init__(self, begin: Point2, mid: Point2, end: Point2):
        self._begin = begin
        self._mid = mid
        self._end = end        
        self._update_status()
            
    def _update_status(self):
        self._last_status = CommandStatus.OK
        if not self.is_valid:
            self._last_status = CommandStatus.FAIL        
        
    # альтернативный конструктор
    def from_center_radius_angles(self, center, radius, angle_begin, angle_and):
        ...
    
    # невалидная если точки на одной прямой
    @property
    def is_valid(self) -> bool:
        return abs(predicate_left_rot(self._begin, self._mid, self._end)) <= EPSILON
    
    @property
    def raw(self):
        return self._begin, self._mid, self._end
    
    @property
    def begin(self) -> Point2:
        return self._begin
    
    @property
    def mid(self) -> Point2:
        return self._mid
    
    @property
    def end(self) -> Point2:
        return self._end
        
    # заглушка! добавить формулы!
    @property
    def radius(self) -> float:
        ans = None
        if self.is_valid:
            return None
        return 0
        
    @property    
    def length(self) -> float:
        ...
        
    @property
    def angle(self) -> float:
        ...
    
    @property
    def angle_beg(self) -> float:
        ...
        
    @property
    def angle_end(self) -> float:
        ...        
        
    @property
    def center(self) -> Point2:
        ...
        
    @property
    def reversed(self) -> Arc2:
        return Arc2(self.end, self.mid, self.begin)
        
    @property
    def last_status(self) -> CommandStatus:
        return self._last_status
    
    def moveB(self, new_B: Point2):
        self._begin = new_B
        if not self.is_valid:
            self._last_status = CommandStatus.FAIL
        self._last_status = CommandStatus.OK
        
    def moveE(self, new_E: Point2):
        self._end = new_E
        if not self.is_valid:
            self._last_status = CommandStatus.FAIL
        self._last_status = CommandStatus.OK        
    
    def transform(self, mat3: Matrix3_raw) -> GeomLinear:
        ...


class Pline2(GeomLinear):
    def __init__(self, pline_raw: Pline2_raw):
        ...
    
    @property
    def last_status(self):
        ...
    
    @property
    def begin(self):
        ...
    
    @property
    def end(self):
        ...
        
    @property
    def reversed(self) -> Pline2:
        ...    
    
    def __getitem__(self, index: int) -> Point2:
        ...
    
    def points_number(self):
        ...
    
    def length(self) -> float:
        ...
        
    def add(self, index: int, p2: Point2):
        ...
        
    def remove(self, index: int, p2: Point2):
        ...
        
    def move(self, index: int, new_p2: Point2):
        ...
    
    def __iter__(self):
        ...
    
    def transform(self, mat3: Matrix3_raw) -> GeomLinear:
        ...
    
    
class LineArcContour2(GeomLinear):
    def __init__(self, epsilon = EPSILON):
        ...
    
    @property
    def last_status(self):
        ...
    
    def add_to_head(self, can_reverse: bool):
        ...
        
    def add_to_tail(self, can_reverse: bool):
        ...
    
    def add_to_nearest(self, can_reverse: bool):
        ...
        
    def remove_from_head(self):
        ...
        
    def remove_from_tail(self):
        ...
        
    @property
    def begin(self) -> Segment2:
        ...
    
    @property
    def end(self) -> Segment2:
        ...    
    
    @property
    def length(self) -> float:
        ...
    
    @property
    def reversed(self) -> LineArcContour2:
        ...
            
    def __getitem__(self, index):
        ...
    
    def __iter__(self):
        ...
        
    def transform(self, mat3: Matrix3_raw) -> GeomLinear:
        ...
    

# аннотации к типам компаса, увы, не сделать, только проверять как предусловие
class DrawingObjectConveter:
    def __init__(self):
        ...
        
    def last_status(self) -> ConverterCommandStatus:
        ...
    
    def convert_to_ks(self, drawing_object: DrawingObject, idrawingobject):
        ...

    def convert_from_ks(self, idrawing_object) -> arc2:
        ...


class ksEditor:
    def __init__(self, app7):
        ...
        
    @property
    def is_active_2d(self) -> bool:
        ...
    
    @property
    def is_active_3d(self) -> bool:
        ...    
        
    @property
    def active_doc2d(self):
        ...
        
    @property
    def active_doc3d(self):
        ...
    
    @property
    def last_status(self):
        ...
    
    @property    
    def selection(self):
        ...    
        

class ksEditor2D(ksEditor):
    def __init__(self, app7):
        ...
    
    def add_drawing_object(self, new_dr_object: DrawingObject):
        ...
    
    def add_hyperlink_to_selection(self, imodelobject, text):
        ...
  
    
class ksEditor3D(ksEditor):
    def __init__(self, app7):
        ...
    
    ...    
