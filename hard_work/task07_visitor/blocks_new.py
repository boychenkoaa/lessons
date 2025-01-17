from enum import Enum

class iBlock():
    def __init__(self):
        pass
    
    def export(self) -> str:
        pass

class PointInterpolationType(Enum):
    UNKNOWN = 0
    LINEAR = 1
    C1 = 2
    C2 = 3
    JOINT = 4
    LINEAR_JOINT = 5
    
PIT = PointInterpolationType

# blocks_new

class movementBlock(iBlock):
    def __init__(self, pt_num: int, interpolation_type: PointInterpolationType, velocity: str):
        super().__init__()
        self.pt_num = pt_num
        self.interpolation_type = interpolation_type
        self.velocity = velocity
                
    def export(self, pp: iPostProcessor) -> str:
        pp.visit_movement(self)     

class SimpleActionType(Enum):
    ARCOF = 1
    KUSAKA = 2
    CLEAN = 3
    
class SimpleActionBlock(iBlock):
    def __init__(self, action_type: SimpleActionType):
        self.action_type = action_type
        
    def export(self, pp: iPostProcessor) -> str:
        return pp.visit_simple_action(self)

class ArconType(Enum):
    SIMPLE = 0
    PROC = 1
    WELD_PARAMETERS = 2
    
class ArconBlock(iBlock):
    def __init__(self, arcon_type: ArconType, arcon_args: str):
        self.arcon_type = arcon_type
        self.arcon_args = arcon_args
        
    def export(self, pp: iPostProcessor) -> str:
        return pp.visit_arcon(self)    

class TouchBlock(iBlock):
    def __init__(self, p8: P8):
        self.p8 = p8
        
    def export(self, pp: iPostProcessor) -> str:
        return pp.visit_touch(self)          

class iPostProcessor:
    def __init__(self):
        ...
        
    def visit_movement(self, block: movementBlock) -> str:
        ...
        
    def visit_arcon(self, block: ArconBlock) -> str:
        ...
        
    def visit_simple_action(self, block: SimpleActionBlock) -> str:
        ...
        
    def visit_touch(self, block: TouchBlock) -> str:
        ...
        

class kwPostprocessor(iPostProcessor):
    def __init__(self):
        self.arcon_prefix = ""
        self.arcon_name = "arcon"
        self.arcon_suffix = ""
        self.z_prefix = ""
        self.arcof_prefix = ""
        self.arcof_suffix = ""
        self.touch_result_varname = "touch_result"
        self.pointmovement_dict = {PIT.UNKNOWN: "?????", PIT.LINEAR: "LMOVE", PIT.C1: "C1MOVE", PIT.C2: "C2MOVE", PIT.JOINT: "?????", PIT.LINEAR_JOINT: "?????"}
    
        
    def visit_movement(self, block: movementBlock) -> str:
        point_varname = "p" + str(block.pt_num)
        ans = ""
        if block.interpolation_type == PIT.LINEAR:
            ans += "SPEED " + to_str(block.p8.v, 1) + " MM/S ALWAYS"
        ans += self.pointmovement_dict[block.interpolation_type] + " " + point_varname
        return ans
    
    def visit_arcon(self, block: ArconBlock) -> str:
        d = {ArconType.SIMPLE: "CALL " + self.arcon_name, \
             ArconType.PROC: "CALL " + self.arcon_name + "(" + block.arcon_args + ")", \
             ArconType.WELD_PARAMETERS: "CALL weld_parameters(" + block.arcon_args+ ")"}
        
        return self.arcon_prefix + d[block.arcon_type] + self.arcon_suffix
        
    def visit_simple_action(self, block: SimpleActionBlock) -> str:
        d = {SimpleActionType.ARCOF: self.arcof_prefix + "CALL arcof" + self.arcof_suffix, SimpleActionType.KUSAKA: "CALL bite", SimpleActionType.CLEAN: "CALL clean"}
        return d[block.action_type]
        

class yPostprocessor(iPostProcessor):
    def __init__(self):
        self.p6_point_prefix = "C"
        self.pos_point_prefix = "EX"
        self.arcon_prefix = ""
        self.arcon_suffix = ""
        self.arcof_prefix = ""
        self.arcof_suffix = ""
    
    def visit_movement(self, block: movementBlock) -> str:
        mov_dict = {PIT.C1: ("MOVC1", self.p6_point_prefix, "V="),\
                    PIT.C2: ("MOVC1", self.p6_point_prefix, "V="),\
                    PIT.JOINT: ("MOVJ", self.p6_point_prefix, "VJ="),\
                    PIT.LINEAR: ("MOVL", self.p6_point_prefix, "V="),\
                    PIT.LINEAR_JOINT: ("MOVL", self.p6_point_prefix, "V=")}
        
        t = mov_dict[block.interpolation_type]
        ans = t[0] + " " + t[1] + str(block.pt_num) + t[2] + block.velocity
        if block.interpolation_type == PIT.LINEAR_JOINT:
            t = mov_dict[PIT.JOINT]
            ans += "+" + t[0] + " " + t[1] + str(block.pt_num) + t[2] + block.velocity
        return ans
        
    def visit_arcon(self, block: ArconBlock) -> str:
        return self.arcon_prefix + 'ARCON' + self.arcon_suffix
        
    def visit_simple_action(self, block: SimpleActionBlock) -> str:
        d = {SimpleActionType.ARCOF: self.arcof_prefix + "ARCOF" + self.arcof_suffix, SimpleActionType.KUSAKA: "CALL cut_wire", SimpleActionType.CLEAN: "CALL clean"}
        return d[block.action_type]
