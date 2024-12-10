from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from geom_raw import * 
from geom2d import * 

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
    NIL = 0
    OK = 1
    ERR = 2
    
class ConverterCommandStatus(Enum):
    UNKNOWN_TYPE = "UNKNOWN_TYPE" 

class ksApp:
    def __init__(self):
        ...
        
    def api7(self):
        ...
        
    def api5(self):
        ...
        
    def is_active(self) -> bool:
        ...

class ksReader:
    def __init__(self, app: ksApp):
        ...
        
    def active_doc(self):
        ...
        
    def is_active_doc2d_fragment(self) -> bool:
        ...
        
    def is_active_doc3d_part(self) -> bool:
        ...
       
    def _toppart(self):
        ...
        
    def _selected_body(self):
        ...
        
    def _all_bodies(self):
        ...
        
    def _selected_or_all_bodies(self):
        ...
    
    def _faces_of_body(self):
        ...
        
    def _model_container(self):
        ...
    
# аннотации к типам компаса, увы, не сделать, только проверять как предусловие
class ksConveter:
    def __init__(self, app7: ksApp):
        ...
        
    def last_status(self) -> ConverterCommandStatus:
        ...
    
    def convert_to_ks(self, drawing_object: DrawingObject, ksdrawingobject):
        ...

    def convert_from_ks(self, idrawing_object) -> DrawingObject:
        ...


class ksCAD:
    def __init__(self, app: ksApp):
        ...

    def reset(self):
        ...

    @property
    def last_status(self):
        ...

    def selection_to_LAC(self):
        ...

    def reverse_LAC(self):
        ...

    def slice(self, slice_parameters):
        ...

    def hide_selection(self):
        ...

    def show_all(self):
        ...

    def set_selection_style(self, style_num):
        ...    

    def LAC_to_autoline(self):
        ...

    def autoline_to_LAC(self):
        ...
 
class ksInterpreter:
    def __init__(app: ksApp):
        ...
        
    def convert(self, ksObject, mode):
        ...
    
    @property
    def last_status(self):
        ...
        
    
class ksCAM:
    def __init__(self, ksreader: ksApp):
        ...
        
    def set_postpropeccor(self):
        ...

    def active_doc(self):
        ...
    
    def set_interpreter_type(self):
        ...
    
    def append_selection(self):
        ...
    
    def append_LAC(self):
        ...
        
    def append_segment(self):
        ...
        
    def append_circle(self):
        ...
        
    def append_selection(self):
        ...
        
    def set_path_properties(self, path_properties):
        ...
        
    def show_BE_markers(self, LAC_only: bool, selection_only: bool):
        ...       


class ksWaamApp:
    def __init__(self, app: ksApp):
        self._cad = ksCAD(app)
        self._cam = ksCAM(app)
        
    def slice(self, h_list: list[float]):
        ...
    
    def reverse_selected_LAC(self):
        ...
    
    
class Job:
    def __init__(self, name: str):
        self._name = name
        
    def append(self, path: RobotPath):
        ...
    
class PathSettings:
    ...
    
class JobSettings:
    ...
    
class PostProcessor:
    ...
    