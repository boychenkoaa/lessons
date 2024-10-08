class GeomContour:
    ...
    
    def nearest_geom_connection(self, new_primitive: GeomPrimitive, connection_params: ConnectionParams) -> GeomConnection:
        
        H, T = self.BE
        B, E = new_primitive.BE
        BH, EH, BT, ET = map(distance_pp, (B, E, B, E), (H, H, T, T))
        GC = GeomConnection
        geom_connection_table = \
            {("HEAD", False): (GC(True, False, EH)), \
            ("HEAD", True): (GC(True, False, EH), GC(True, True, BH)), \
            ("TAIL", False): (GC(False, False, BT)), \
            ("TAIL", True): (GC(False, False, BT), GC(False, True, ET)), \ 
            ("ANY", False): (GC(True, False, EH), GC(False, False, BT)),  \
            ("ANY", True): (GC(True, False, EH), GC(True, True, BH), GC(False, False, BT), GC(False, True, ET)) \
            }
        connection_type, try_reverse = connection_params.connection_point_type, connection_params.try_reverse
        return GeomConnection(min(geom_connection_table[(connection_type, try_reverse)], key = lambda gc: gc.distance)
