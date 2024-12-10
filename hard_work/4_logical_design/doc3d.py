from kompas_base import *
from global_var import * 
from collections import namedtuple
from functools import reduce
from base import fold
# все манипуляции производятся только с toppart7
# из него же можно извлечь контейнер вспомогательной геометрии IAuxillaruGeomcontainer

command_status = namedtuple("command_status", ["command_name", "is_ok"])
query_status = namedtuple("query_status", ["query_name", "is_ok"])
    
class KompasManipulator3D:
    def __init__(self, app: KompasApp):
        self._app = app
        self._status_stack = []
    
    @property
    def api7(self):
        return self._app.api7
    
    @property
    def object5(self):
        return self._app.object5
    
    @property
    def const3d(self):
        return self._app.constants_3d
    
    
    def to5(self, object):
        return self._app.to5(object)
    
    @property
    def active_doc3d(self):
        return self._app.active_doc3d
    
    @property
    def toppart7(self):
        return self.active_doc3d.TopPart
    
    def bodies_of_part(self, ipart7):
        api7 =  self._app.api7
        ifeature7 = api7.IFeature7(ipart7)
        bodies = ifeature7.ResultBodies
        return to_tuple(bodies)
    
    def selection3d(self, types:list|None = None):
        sel = to_tuple(self.active_doc3d.SelectionManager.SelectedObjects)
        return sel if types == None else tuple(filter(lambda obj: obj.Type in types, sel))
    
    @property
    def selected_bodies(self):
        return self.selection3d([11009])
    
    @property
    def body_for_slicing(self):
        all_bodies = to_tuple(self.api7.IFeature7(self.toppart7).ResultBodies)
        if len(all_bodies) == 1:
            return all_bodies[0]
        sb = self.selected_bodies
        if len(sb) == 1:
            return sb[0]
        return None
    
    def faces_of_body(self, ibody7):
        return self.api7.IFeature7(ibody7).ModelObjects(self.const3d.o3d_face)            
    
    @property
    def faces_for_slicing(self):
        body = self.body_for_slicing
        if body == None:
            return None
        return self.faces_of_body(self.body_for_slicing)
    
    # sic = surfaces intersecton curve
    def add_sic(self, surfaces_list1, surfaces_list2) -> tuple:
        new_curve = self.aux_container.SurfacesIntersectionCurves.Add()
        new_curve.AddObjects(True, surfaces_list1)
        new_curve.AddObjects(False, surfaces_list2)
        is_ok = new_curve.Update()
        return new_curve, is_ok
    
    def _plane_name(self, name_base: str, z: float):
        return "{} | z = {:.2f}".format(name_base, z)
    
    def _create_plane_z_offset(self, base_plane, plane_name: str, z_offset: float):
        new_plane = self.aux_container.Planes3D.Add(self.const3d.o3d_planeOffset)
        op = self.api7.IPlane3DByOffset(new_plane)
        op.BasePlane, op.Direction, op.Offset, op.Name = base_plane, True, z_offset, plane_name
        op.Update()
        return op    
    
    def slice_planes(self, z_offset_list: list[float], name_base: str):
        return [self._create_plane_z_offset(self.active_xy_plane, plane_name = self._plane_name(name_base, z), z_offset = z) for z in z_offset_list]
    
    @property
    def aux_container(self):
        return self.api7.IAuxiliaryGeomContainer(self.toppart7)
    
    @property
    def model_container(self):
        return self.api7.IModelContainer(self.toppart7)
    
    # возвращает либо текущую ЛСК (o3d_localCoordinateSystem = 85) либо Мировую (o3d_pointCS = 4)
    @property
    def active_cs(self):
        return self.aux_container.LocalCoordinateSystems.Current
    
    @property
    def active_xy_plane(self):
        parent = self.api7.ILocalCoordinateSystem(self.active_cs) if self.active_cs.ModelObjectType == self.const3d.o3d_localCoordinateSystem else self.toppart7
        return self.api7.IPlane3D(parent.DefaultObject(self.const3d.o3d_planeXOY))
           
    def add_sketch(self, base_plane, name: str):
        new_sketch = self.model_container.Sketchs.Add()
        new_sketch.Plane = base_plane
        new_sketch.Name = name
        new_sketch.CoordinateSystem = self.active_cs
        new_sketch.Angle = 0
        new_sketch.Update()
        return new_sketch
    
    def slice_name(self, base_name: str, slice_num: int, z: float):
        return "{}_{:d}_{:.2f}".format(base_name, slice_num, z)
    
    def ic_to_sketch(self, sketch, ic):
        edges = (fold([to_tuple(ic.Edges(i)) for i in range(ic.EdgesArraysCount)]))
        sketch.BeginEdit()
        ans = [sketch.AddProjectionOf(edge.MathCurve) for edge in edges]
        sketch.EndEdit()
        return ans    
        
    def add_arrows_to_sketch(self, sketch):
        sketch.BeginEdit()
        styles_manager = self.api7.IStylesManager(self.api7.IKompasDocument (self._app.active_doc2d))
        curves_styles =  styles_manager.CurvesStyles
        istyles = self.api7.IStyles(curves_styles)
        lib_filename = ARROW_STYLE_FILENAME
        arrow5_style = istyles.AddStyleFromLibrary (lib_filename, ARROW5_ID, True)
        arrow1_style = istyles.AddStyleFromLibrary (lib_filename, ARROW1_ID, True)
        return (arrow1_style != None) and (arrow5_style != None)        
    
    def hide_modelobject(self, modelobject):
        # если макрообъект
        if modelobject.Type == 11289:
            for obj in to_tuple(modelobject.Objects):
                self.hide_modelobject(obj)             
        
        modelobject.Hidden = True
        modelobject.Update()
    
    def hide_selection(self):
        for mo in self.selection3d():
            self.hide_modelobject(mo)
                    
    def add_macroobject(self, name:str, objects_tuple: tuple):
        container = self.model_container.MacroObjects3D
        new_macro = container.Add()
        new_macro.StaffVisible = True
        new_macro.DoubleClickEditable = False
        new_macro.Objects = objects_tuple
        new_macro.Name = name
        new_macro.Update()
        self.active_doc3d.RebuildDocument()
        return new_macro
        
    # TODO
    # добавить стрелочки
    def slice1(self, z_list:list[float], name: str):
        planes_list = self.slice_planes(z_list, name)
        faces = self.faces_for_slicing
        if faces == None:
            return False
        sic_tuple_list = [self.add_sic(plane, self.faces_for_slicing) for plane in planes_list]
        sic_list = [t[0] for t in sic_tuple_list]
        sk_list = []
        for i in range(len(sic_list)):
            sketch = self.add_sketch(planes_list[i], self.slice_name(name, i, z_list[i]))
            sic = sic_list[i]
            self.add_arrows_to_sketch(sketch)
            self.ic_to_sketch(sketch, sic)
            sketch.Update()            
            self.api7.IFeature7(sic).Delete()
            sketch.DeleteWrongProjection()
            sk_list.append(sketch)
        self.add_macroobject(name + " плоскости", planes_list)
        self.add_macroobject(name + " эксизы", sk_list)
        return True

