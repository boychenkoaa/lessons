# вспомогательные классы
class AnyHeadTail(Enum):
    ANY = "ANY"
    HEAD = "HEAD"
    TAIL = "TAIL"

@dataclass
class ConnectionParams:
    connection_point_type: AnyHeadTail
    repair_type: RepairType
    try_reverse: bool = True

@dataclass
class GeomConnection:
    to_head: bool = False
    is_reversed: bool = True
    distance: float = EPSILON

# лечим метод nearest_geom_connection
class GeomContour:
    ...
    def nearest_geom_connection(self, new_primitive: GeomPrimitive, connection_params: ConnectionParams) -> GeomConnection:
        d = distance_pp
        H, T = self.BE
        B, E = new_primitive.BE
        BH, EH, BT, ET = d(B, H), d(E, H), d(B, T), d(E, T)
        
        ans = None
        connection_type, try_reverse = add_info.connection_point_type, 
        if connection_type == AnyHeadTail.HEAD:
            ans = GeomConnection(is_head = True, is_reversed = False, distance = EH)
            if try_reverse and BH < EH:
                ans.is_reversed = True
                ans.distance = BH
        
        elif connection_type == AnyHeadTail.TAIL:
            ans = GeomConnection(is_head = False, is_reversed = False, distance = BT)
            if try_reverse and ET < BT:
                ans.is_reversed = True
                ans.distance = ET
        
        elif connection_type == AnyHeadTail.ANY:
            ans = GeomConnection(is_head = True, is_reversed = False, distance = EH)
            if BT < EH:
                ans.to_head = False
                ans.distance = BT
            
            if try_reverse:
                if BH < ans.distance:
                    ans.to_head = True
                    ans.is_reversed = True
                    ans.distance = BH
                if ET < ans.distance:
                    ans.to_head = False
                    ans.is_reversed = True
                    ans.distance = ET
        return ans