## Отчет

## 1. Методы, используемые только в тестах

**тип 1.** Устаревшие методы-времянки, отражающие промежуточное состояние,
например, встретилось такое чудо
```
class Manipulator2D	
	def linestyle(self, style_num: int):
        if style_num == None:
            return self.DefaultLineStyle
    return style_num
```
нужно вынести их из класса в другой уровень: либо унаследоваться (что на самом деле криво)
либо сделать их методами класса-наследника от TestCase и ему подобных
**способ 1**
```
class ForTestManipulator2D(Manipulator2D)
	def repair_linestyle(self, style_num: int|None) -> int:
        if style_num == None:
            return self.DefaultLineStyle
        return style_num
```

**способ 2**
```
class TestManipulator2D(Unittest.TestCase)
	def repair_linestyle(self, manipulator, style_num: int|None) -> int:
        if style_num == None:
            return self.DefaultLineStyle
        return style_num
```

Мне если честно, оба способа кажутся пока что кривыми

-  псевдо-моки: когда в класс включаются "имитаторы" функциональности других классов для тестирования их взаимодействия
решение -- писать полноценные моки

### цепочки методов
основной метод
```
def slice(self, z_list:list[float], name: str):
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
```
для краткости, не буду приводить полный код:
цепочка вызовов
slice -> faces_for_slicing ->  faces_of_body -> body_for_slicing -> selected_bodies -> selection3d

цепочку  faces_of_body -> body_for_slicing -> selected_bodies  можно убрать в
faces_for_slicing




```
def faces_for_slicing(self) -> list:
    O3D_BODY, O3D_FACE = self.const3d.o3d_body, self.const3d.o3d_face
	active_bodies = self.selection3d([self.const3d.o3d_body])
	# если не выделены тела, то слайсятся все 
    # не очень правильно сделано
    # такие решения должны приниматься уровнем выше, но видимо это будет на следующем занятии :)
    
    if len(active_bodies == 0):
		active_bodies = to_tuple(self.api7.IFeature7(self.toppart7).ResultBodies)

	ans = sum(	[self.api7.IFeature7(ibody7).ModelObjects(O3D_FACE) for ibody7 in active_bodies], start = [])
    return ans
```

##  Слишком большой список параметров 

было вылечено давно, но тем не менее
```

class pointBlock(iBlock):
    def __init__(self, pt_num: int, x: float,y: float,z:float,o:float,a:float,t:float,p1:float,p2:float):
        super().__init__()
        self.pt_num = pt_num
        self.x = x
        self.y = y
        self.z = z
        self.o = o
        self.a = a
	    ...
    
```

группируем данные в простейшие NamedTuple  -- и иммутабельные, и быстро пишется (автор этого класса явно любил ЛИСП)

```
rPoint8 = NamedTuple("rPoint8", [("x", float), ("y", float), ("z", float),("o", float), ("a", float), ("t", float),("p1", float),("p2", float)])
```
конструктор теперь упрощается

```
class pointBlock(iBlock):
    def __init__(self, pt_num: int, rpoint8: rPoint8):
        super().__init__()
        self.pt_num = pt_num
        self.point8 = rpoint8
```

## Странные решения: дублирование методов

Излишний функционал

```

class Graph:
	# предусловие: на входе действительно подмножество
	def reject(self, id_subset:set[int]):
		...

	# предусловие: на входе действительно подмножество
	# 
	def subgraph(self, id_subset:set[int]) -> Graph:
		if ...:
			self._c_status = Statue.ERR
			return None
		return deepcopy(self).reject(id_subset)

```

Наверное, все же, следовало бы оставить только `subgraph`, он не меняет внутреннее состояние основного объекта, а при большом желании делать присваивание
```
from __future__ import annotations

class Graph:
	
	def subgraph(self, id_set:set[int]) -> Graph:
		ans = deepcopy(self)
		...
		# все что было внутри старого reject
		...
		return ans

```

## Чрезмерный результат

из некритичного, у меня есть чрезмерный результат, заложенный на будущее
`snaked_pline` помимо координат точек несет в себе доп. информацию
```

def snakes_of_polygon(polygon: Polygon2, distances: list[float], angle: float):
    ...
    
    rp_snakes = [raster.snaked_pline for raster in raster_levels.all_rasters]

    # в дальнейшем эта инфа может пригодиться, но пока что она лишняя, отрезаем
    ans =  [[rp.point for rp in rp_snake] for rp_snake in rp_snakes]
    return ans
```

Исправить можно, добавив метод `snake_points` как урезанную версию `snaked_pline` в иерархии выше.

```
class Raster:
	@property
	def snaked_pline(self):
		...

	@property
	def snake_points(self)
		return [rp.point for point in self.snaked_pline]


def snakes_of_polygon(polygon: Polygon2, distances: list[float], angle: float) -> list[Pline2]:
	
	...
	
	ans = [raster.snake_points for raster in raster_levels.all_rasters]

	return ans
```
