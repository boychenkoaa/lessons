from geom2d_base import add, sub, perpendiculat_vec

Segment2 = tuple[Point2, Point2]
Triangle2 = tuple[Point2, Point2, Point2]
MESH_TRIANGLE_HEIGHT = 0.1

class Mesh2D:
    def __init__(self):
	    self._faces = set()
		self._verts = set()
		self._edges = set()

    def from_triangles(self, triangles_list: list[Triangle2]):
        ...

class ToMeshMixin:
	@property
  	def  segments(self) -> list[Segment2]:
        	raise NotImplementedError()
  
  	def triangulate_segment(self, segment: Segment2) -> list[Triangle2]:
  		beg, end = segment
  		v_p = mul(perpendicular_vec(sub(beg, end)), 0.1)
  		tri1 = Triangle2(add(beg, v_p), beg, end)
  		tri2 = Triangle2(sub(end, v_p), end, beg)
  		return [tri1, tri2]
  
  	def to_mesh(self) -> Mesh2D:
  		return Mesh2D().from_triangles(sum([triangulate_segment(segment) for segment in self.segments], start = []))
  
  # примесь для печати в матплотлибе
  class PlotMixin:
  	  @property
  	  def segments(self) -> list[Segment2]:
          raise NotImplementedError()
  		
   	  def plot(self, plt, **kwargs)
          for segment in segments:
              plt.plot([segment[B][X], segment[E][X]],[segment[B][Y], segment[E], [Y]], **kwwagrs)

  # абстрактная геометрия
  class Geometry2D:
      ...
  	  @property
  	  def segments(self):
          raise NotImplementedError()

  # пример
  class ProjectPline2D(Geometry2D, ToMeshMixin, PlotMixin):
  	  ...
  	  def segments(self):
          return list(zip(self.points, self.points[1:]))
