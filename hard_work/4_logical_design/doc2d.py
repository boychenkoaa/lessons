from kompas_base import *
from geom2d_base import *
from base import *
from global_var import * 
from points1 import *
from postrpoc1 import *
from snake import snake
    

class KompasManipulator2D:
    def __init__(self, app: KompasApp):
        self._app = app
        self.DefaultLineStyle = self._app.constants.ksCSNormal
        self.parent_doc3d = self._app.active_doc3d   
    
    @property
    def api7(self):
        return self._app.api7
    
    @property
    def active_doc2d(self):
        return self._app.active_doc2d
    
    def update_parentdoc3d(self):
        self.parent_doc3d = self._app.active_doc3d   
        
    def to5(self, object7):
        return self._app.to5(object7)
    
    @property
    def active_plane_offset(self):
        app = self._app
        idoc3d = self.parent_doc3d
        if idoc3d == None or idoc3d.DocumentType != app.constants.ksDocumentPart:
            return None
        
        idoc3d1 = app.api7.IKompasDocument3D1(idoc3d)
        eo = idoc3d1.EditObject
        if eo==None or eo.FeatureType != app.constants_3d.o3d_entity:
            return None
            
        mo = app.api7.IModelObject(eo)
        if mo.ModelObjectType != app.constants_3d.o3d_sketch:
            return None
            
        sk = app.api7.ISketch(mo)
        plane = sk.Plane
        if plane.ModelObjectType != app.constants_3d.o3d_planeOffset:
            return None
        
        plane3d = app.api7.IPlane3DByOffset(plane)
        return plane3d.Offset
    
    def add_macroobject_to_parent3d(self, name):
        model_container = self.api7.IModelContainer(self.parent_doc3d.TopPart)
        container = model_container.MacroObjects3D
        new_macro = container.Add()
        new_macro.StaffVisible = True
        new_macro.DoubleClickEditable = False
        new_macro.Name = name
        new_macro.Update()
        self.parent_doc3d.RebuildDocument()
        return new_macro
    
    def linestyle(self, style_num: int):
        if style_num == None:
            return self.DefaultLineStyle
        return style_num
        
    def insert_arrow_to_active_doc(self):
        styles_manager = self.api7.IStylesManager(self.active_doc2d)
        curves_styles =  styles_manager.CurvesStyles
        istyles = self.app.api7.IStyles(curves_styles)
        lib_filename = ARROW_STYLE_FILENAME
        arrow5_style = istyles.AddStyleFromLibrary (lib_filename, 32805, True)
        arrow1_style = istyles.AddStyleFromLibrary (lib_filename, 32801, True)
        return (arrow1_style != None) and (arrow5_style != None)          
        
    @property
    def active_view(self):
        return self.active_doc2d.ViewsAndLayersManager.Views.ActiveView
        
    def layer(self, layer_num: int):
        return self.active_view.Layers.LayerByNumber(layer_num)
    
    def layer_comment(self, layer_num: int):
        return self.layer(layer_num).Comment    
    
    @property
    def drawing_container(self):
        return self.api7.IDrawingContainer(self.active_view)        
        
    def selection2d(self, types: list|None = None):
        selection = to_tuple(self.api7.IKompasDocument2D1(self.active_doc2d).SelectionManager.SelectedObjects)
        if types != None:
            selection = tuple(filter(lambda obj: obj.Type in types, selection)) 
        return selection

    def repair_slice_simple(self, epsilon = 0.1):
        sp = StrangePoints(epsilon, 2)
        dr_container = self.drawing_container
        ipoints = dr_container.Points
        sketch_points =  to_tuple(dr_container.Objects(5))
        for ipoint in sketch_points:
            xy = ipoint.X, ipoint.Y
            ref = ipoint.Reference 
            # если близкой точки нет, то просто добавит и условие не сработает
            # если есть то ищещ соседа, удаляет себя и его из детектора и из чертежа
            if not sp.add(xy, ref):
                xy2, ref2 = sp.nearest_pointext(xy)
                self.add_linesegment(xy, xy2)
                sp.remove(xy)
                ipoint.Delete()
                ipoints.Point(ref2).Delete()   
    
    # True если успешно
    def insert_hyperlink(self, drawing_objects, text):
        a_doc2d = self.active_doc2d
        a_doc2d1 =  self.api7.IKompasDocument2D1(a_doc2d)
        return a_doc2d1.CreateHyperLink(drawing_objects, 1, text, None, 0)    
    
    # подходят для кривых и контуров
    # eps - точность аппроксимации (от 1e-7 до 1)
    # False - на слой кривой (True - на текущий активный)
    # max_rad - максимальный радиус дуги (можно делать малым, 0.1 например, чтобы были только отрезки)
    # False -- негладкое сопряжение (smooth)
    # возвращает референс на аппроксимированную кривую
    def approximate_curve(self, curve, eps, max_rad) -> int:
        return self.to5(self.active_doc2d).ksApproximationCurve(curve.Reference, eps, False, max_rad, False)
    
    def add_point(self, xy: Point2, point_style: int = 0):
        new_point = self.drawing_container.Points.Add()
        new_point.X, new_point.Y = xy
        new_point.Style = point_style
        return new_point.Update(), new_point
    
    def show_BE_of_contour(self, dr_contour):
        be = self.drawing_object_BE(dr_contour)
        self.add_point(be[0], 6)
        self.add_point(be[1], 3)
        
    def delete_all_points(self):
        for ipoint in self.drawing_container.Points:
            ipoint.Delete()
            
    def update_BE_of_contours(self):
        self.delete_all_points()
        for dr_contour in self.drawing_container.DrawingContours:
            self.show_BE_of_contour(dr_contour)
    
    def add_linesegment(self, begin, end):
        new_seg = self.drawing_container.LineSegments.Add()
        new_seg.X1, new_seg.Y1 = begin
        new_seg.X2, new_seg.Y2 = end
        update_is_successful = new_seg.Update()
        return update_is_successful, new_seg
    
    def add_arc(self, begin, mid, end):
        new_arc = self.drawing_container.Arcs.Add()
        new_arc.X1, new_arc.Y1 = begin
        new_arc.X2, new_arc.Y2 = mid
        new_arc.X3, new_arc.Y3 = end
        update_is_successful =  new_arc.Update()
        return update_is_successful, new_arc
        
    def add_LA(self, seg23: tuple[float]):
        if len(seg23) == 2:
            return self.add_linesegment(*seg23)
        if len(seg23) == 3:
            return self.add_arc(*seg23)
        return False
    
    def constraints_of(self, dr_object):
        return [self.api7.IParametriticConstraint(c) for c in to_tuple(self.api7.IDrawingObject1(dr_object).Constraints)]
    
    def nb_constraints_of(self, dr_object):
        return list(filter (lambda c: c.ConstraintType == MERGE_POINT_CONSTRAINT_TYPE, self.constraints_of(dr_object)))
    
    def nb_of(self, dr_object):
        constraints =  self.nb_constraints_of(dr_object)
        return tuple([c.Partner[0] for c in constraints])
    
    # поиск по сопряжениям
    # связь не означает направление
    def connected_chain(self, first_segment):
        nb = self.nb_of(first_segment)
        if len(nb) != 1:
            return [first_segment]
        ans = [first_segment, nb[0]]
        
        nb =  self.nb_of(ans[-1])
        while len(nb) == 2:
            new_elem = nb[0] if nb[1].Reference == ans[-2].Reference else nb[1]
            ans.append(new_elem)
            nb = self.nb_of(ans[-1])
        return ans
        
    def layer_str_of(self, dr_object):
        return '{' + self.layer_comment(dr_object.LayerNumber) + '}'
    
    def hlink_str_of(self, dr_object):
        return '{' + self.api7.IDrawingObject1(dr_object).GetHyperLinkParam()[0] + '}'
        
    def reverse_linesegment(self, linesegment):
        new_ls = self.drawing_container.LineSegments.Add()
        new_ls.X1, new_ls.X2 = linesegment.X2, linesegment.X1
        new_ls.Y1, new_ls.Y2 = linesegment.Y2, linesegment.Y1
        is_ok = new_ls.Update()
        if is_ok:
            linesegment.Delete()
        return (is_ok, new_ls)
        
    def reverse_arc(self, arc):
        add_is_ok, new_arc = self.add_arc((arc.X2, arc.Y2), (arc.X3, arc.Y3), (arc.X1, arc.Y1))
        if add_is_ok:
            new_arc.Style = arc.Style
            new_arc.Update()
            arc.Delete()
        return add_is_ok, new_arc
            
    def ilinesegment_raw(self, linesegment):
        return (linesegment.X1, linesegment.Y1), (linesegment.X2, linesegment.Y2)
    
    def iarc_raw(self, arc):
        return (arc.X1, arc.Y1), (arc.X3, arc.Y3), (arc.X2, arc.Y2)
    
    def icontour_is_LA(self, icontour):
        return all ([(obj.Type == LINESEGMENT2) or (obj.Type == ARC2 ) for obj in to_tuple(icontour.TmpObjects)])
    
    def idrawing_object_to_raw(self, drawing_object):
        if drawing_object.Type == LINESEGMENT2:
            return self.ilinesegment_raw(drawing_object)
        elif drawing_object.Type == ARC2:
            return self.iarc_raw(drawing_object)
        return None
    
    def icontourLA_raw(self, icontour):
        if not self.icontour_is_LA(icontour):
            return None
        return [self.idrawing_object_to_raw(dr_obj) for dr_obj in to_tuple(icontour.TmpObjects)]
    
    def reverse_drcontourLA(self, dr_contour):
        icontour = self.api7.IContour(dr_contour)
        if not self.icontour_is_LA(icontour):
            return (False, None)
        c_raw =  self.icontourLA_raw(icontour)
        new_LA_list = []
        for seg in c_raw[::-1]:
            add_succesful, new_seg = self.add_LA(seg)
            if not add_succesful:
                for new_LA in new_LA_list:
                    new_LA.Delete()                
                return (False, None)
            else:
                new_LA_list.append(new_seg)
            
        new_dr_contour = self.drawing_container.DrawingContours.Add()
        new_dr_contour.Style =  dr_contour.Style
        new_icontour = self.api7.IContour(new_dr_contour)
        ans = new_icontour.CopySegments(new_LA_list, True) and new_dr_contour.Update()
        if ans:
            dr_contour.Delete()
        return ans, new_dr_contour        
    
    #test
    def drawing_object_BE(self, drawing_object):
        do = drawing_object
        if drawing_object.Type == 13025:
            return (do.X1, do.Y1), (do.X2, do.Y2)
        
        curve = self.api7.IDrawingObject1(do).GetCurve2D()
        b, e = curve.PointOn(curve.ParamMin), curve.PointOn(curve.ParamMax) 
        return (b[1], b[2]), (e[1], e[2])
    
    
    def dr_contour_to_SketchPath2Dv2(self, dr_contour) -> SketchPath2d:
        icontour = self.api7.IContour(dr_contour)
        dr_objects = to_tuple(icontour.TmpObjects)
        xyt_list = [(*self.drawing_object_BE(dr_objects[0])[0], MOVL)]
        for dr_object in dr_objects:
            if dr_object.Type == LINESEGMENT2:
                xyt_list.append((dr_object.X2, dr_object.Y2, MOVL))
            elif dr_object.Type == ARC2:
                xyt_list.append((dr_object.X3, dr_object.Y3, MOVC1))
                xyt_list.append((dr_object.X2, dr_object.Y2, MOVC2))
            else:
                return None
                
        hyper_strings = [self.hlink_str_of(dr_contour)]
        layer_strings = [self.layer_str_of(dr_contour)]
        z =  self.active_plane_offset
        return SketchPath2d(xyt_list, z, hyper_strings, layer_strings)    
    
    
    def autoline_to_SketchPath2d(self, linesegment) -> SketchPath2d:
        chain = self.connected_chain(linesegment)
        if chain[0].Type != LINESEGMENT2:
            return None
        
        constraints = self.nb_constraints_of(chain[0])
        if len(constraints) >= 2:
            return None
        
        # если этого не сделать, случится беда!
        need_to_reverse_first = (len(constraints) == 1) and constraints[0].Index == 0
        # если конец смотрит наружу
        xyt_list = [(chain[0].X2, chain[0].Y2, MOVL), (chain[0].X1, chain[0].Y1, MOVL)] if need_to_reverse_first else [(chain[0].X1, chain[0].Y1, MOVL), (chain[0].X2, chain[0].Y2, MOVL)]
        hyper_strings = [self.hlink_str_of(chain[0])]
        layer_strings = [self.layer_str_of(chain[0])]       
        for elem in chain[1:]:
            new_point = (elem.X2, elem.Y2) if distance_pp((elem.X1, elem.Y1), (xyt_list[-1][0], xyt_list[-1][1])) <= 0.01 else (elem.X1, elem.Y1)
            if elem.Type == LINESEGMENT2:
                xyt_list.append((*new_point, MOVL))
                hyper_strings.append(self.hlink_str_of(elem))
                layer_strings.append(self.layer_str_of(elem))
            elif elem.Type == ARC2:
                xyt_list.append((elem.X3, elem.Y3, MOVC1))
                xyt_list.append((*new_point, MOVC2))
                hyper_strings.append(self.hlink_str_of(elem))
                layer_strings.append(self.layer_str_of(elem))
                hyper_strings.append(self.hlink_str_of(elem))
                layer_strings.append(self.layer_str_of(elem))                
            else:
                return None

        z =  self.active_plane_offset
        return SketchPath2d(xyt_list, z, hyper_strings, layer_strings)    
    
    def add_autolineL(self, xy_list: list[tuple[float, float]]):
        N = len(xy_list)
        ls_list = [None] * (N - 1)
        for i in range(1, N):
            new_s = self.drawing_container.LineSegments.Add()
            new_s.X1, new_s.Y1, new_s.X2, new_s.Y2 = *xy_list[i-1], *xy_list[i]
            new_s.Update()
            ls_list[i-1] = new_s
        # их тут N-2 штуки если что
        are_ok = [self.add_2LA_merge_constraint(ls_list[i-1], ls_list[i]) for i in range(1, N-1)]
        return (all(are_ok), ls_list[0])
    
    def add_contour_from_xy_list(self, xy_list):
        new_contour = self.drawing_container.DrawingContours.Add()
        new_icontour = self.api7.IContour(new_contour)
        new_icontour.CopySegments([self.add_linesegment(xy_list[i-1], xy_list[i])[1] for i in range(1, len(xy_list))], True)
        return new_contour.Update()
         
    def add_snake_of_xy_list(self, contour: list[tuple[float, float]], angle, step):
        return self.add_contour_from_xy_list(snake(contour, angle, step))
    
    def linearized_contour(self, dr_contour):
        ans = []
        icontour = self.api7.IContour(dr_contour)
        for obj in icontour.TmpObjects:
            if obj.Type == LINESEGMENT2:
                ans.append((obj.X2, obj.Y2))
            else:
                curve = self.api7.IDrawingObject1(obj).GetCurve2D()
                float_list = curve.CalculatePolygonByStep(1.0)
                xy_list = list(zip(float_list[0::2], float_list[1::2]))
                ans.extend(xy_list[1:])
        return ans
    
    def insert_snake_of_dr_contour(self, dr_contour, angle, step):
        self.add_snake_of_xy_list(self.linearized_contour(dr_contour), angle, step)
    
    def LA_to_seg23(sef, dr_object):
        if dr_object.Type == LINESEGMENT2:
            return [(dr_object.X1, dr_object.Y1), (dr_object.X2, dr_object.Y2)]
        elif dr_object.Type == ARC2:
            return [(dr_object.X1, dr_object.Y1), (dr_object.X3, dr_object.Y3), (dr_object.X2, dr_object.Y2)]
        return None
        
    def save_tmp_LA(self, tmp_obj):
        raw = self.LA_to_seg23 (tmp_obj)
        if raw == None:
            return (False, None)
        return self.add_LA(raw)
    
    # если нельзя создать ограничение, вернет  False
    def add_2LA_merge_constraint(self, dr_object_first, dr_object_second):
        if dr_object_first.Type != LINESEGMENT2 and dr_object_second.Type != LINESEGMENT2 and dr_object_first.Type != ARC2 and dr_object_second.Type != AR2:
            return False
        dro1 = self.api7.IDrawingObject1(dr_object_first)
        new_c = dro1.NewConstraint()
        new_c.ConstraintType = MERGE_POINT_CONSTRAINT_TYPE
        new_c.Partner = dr_object_second
        new_c.Index = 1 if dr_object_first.Type == LINESEGMENT2 else 2
        new_c.PartnerIndex = 0 if dr_object_second.Type == LINESEGMENT2 else 1
        return new_c.Create()
      
    def add_snake_of_dr_object(self, dr_object, angle, step):
        curve = self.api7.IDrawingObject1(dr_object).GetCurve2D()
        float_list = curve.CalculatePolygonByStep(1)
        xy_list = zip(float_list[0::2], float_list[1::2])
        return self.add_snake_of_xy_list(xy_list, angle, step)    
        
    # test!
    def pline2d_to_SketchPath2d(self, ipolyline2d) -> SketchPath2d:
        co = ipolyline2d.Points
        xy_list = zip(co[0::2], co[1::2])
        hyper_strings = [self.hlink_str_of(ipolyline2d)]
        layer_strings = [self.layer_str_of(ipolyline2d)]
        z =  self.active_plane_offset
        xyt_list = [(xy[0], xy[1], 0) for xy in xy_list]
        return SketchPath2d(xyt_list, z, hyper_strings, layer_strings)        
        
    # предусмотреть полилинию
    def dr_object_to_SketchPath2D(self, dr_object) -> SketchPath2d:
        convert_func_dict = {PLINE2: self.pline2d_to_SketchPath2d, CONTOUR2: self.dr_contour_to_SketchPath2Dv2, LINESEGMENT2: self.autoline_to_SketchPath2d}
        convert_func = convert_func_dict.get(dr_object.Type)
        if convert_func == None:
            return None
        return convert_func(dr_object)
    
    def reverse_dr_object(self, dr_object):
        reverse_funcs = {LINESEGMENT2: self.reverse_linesegment, ARC2: self.reverse_arc, CONTOUR2: self.reverse_drcontourLA}
        reverse_func = reverse_funcs.get(dr_object.Type)
        if reverse_func==None:
            return (False, None)
        return reverse_func(dr_object)
            
    def reverse_selection(self):
        selection2d = self.selection2d()
        if not selection2d:
            return []
        ans =  [self.reverse_dr_object(dr_object) for dr_object in self.selection2d()]
        self.update_BE_of_contours()
        return ans
    
    def dr_contourLA_to_autoline(self, dr_contour):
        icontour = self.api7.IContour(dr_contour)
        if not self.icontour_is_LA:
            return (False, None)
        result_list = [self.save_tmp_LA(tmp_obj) for tmp_obj in to_tuple(icontour.TmpObjects)]
        good_la_list = [result[1] for result in result_list if result[0]]
        if len(good_la_list) != len(result_list):
            for good_la in good_la_list:
                good_la.Delete()
            return (False, None)
        N = len(good_la_list)
        is_ok_constraints = [self.add_2LA_merge_constraint(good_la_list[i-1], good_la_list[i]) for i in range(1, N)]
        all_is_ok = all(is_ok_constraints)
        if all_is_ok:
            dr_contour.Delete()
        return [all_is_ok, good_la_list[0]]