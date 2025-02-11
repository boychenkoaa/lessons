## Отчет

## 1. Методы, используемые только в тестах
Из такого у меня есть устаревшие методы-времянки, отражающие промежуточное состояние, например, встретилось такое чудо
```
class Manipulator2D:
    ....
    def linestyle(self, style_num: int):
        if style_num == None:
            return self.DefaultLineStyle
    return style_num
```
нужно вынести их из класса в другой уровень: либо унаследоваться
```
class ForTestManipulator2D(Manipulator2D)
    def repair_linestyle(self, style_num: int|None) -> int:
        if style_num == None:
            return self.DefaultLineStyle
    return style_num
```
либо сделать их методами класса-тестировщика
```
class TestManipulator2D(Unittest.TestCase)
    def repair_linestyle(self, manipulator, style_num: int|None) -> int:
        if style_num == None:
            return self.DefaultLineStyle
        return style_num
```
Мне если честно, оба способа кажутся пока что кривыми
Еще один случай (прочитал в интернете) -- "псевдо-моки": когда в класс включаются "имитаторы" функциональности других классов для тестирования их взаимодействия
решение -- писать полноценные моки

## 2. Цепочки методов
Основной метод
```
def slice(self, z_list:list[float], name: str):
    planes_list = self.slice_planes(z_list, name)
    faces = self.faces_for_slicing
    ...
```
Для краткости, не буду приводить полный код.

Цепочка вызовов изначальная: `slice -> faces_for_slicing ->  faces_of_body -> body_for_slicing -> selected_bodies -> selection3d`.

Цепочку  `faces_of_body -> body_for_slicing -> selected_bodies`  можно свернуть в `faces_for_slicing`.

```
def faces_for_slicing(self) -> list:
    O3D_BODY, O3D_FACE = self.const3d.o3d_body, self.const3d.o3d_face
    active_bodies = self.selection3d([O3D_BODY])
    # если не выделены тела, то слайсятся все 
    # не очень правильно сделано
    # такие решения должны приниматься уровнем выше, но видимо это будет на следующем занятии :)
	if len(active_bodies == 0):
        active_bodies = to_tuple(self.api7.IFeature7(self.toppart7).ResultBodies)

    ans = sum([self.api7.IFeature7(ibody7).ModelObjects(O3D_FACE) for ibody7 in active_bodies], start = [])
    return ans
```

##  3. Слишком большой список параметров 
Классика, все уже давно вылечено, приведу пример
```
class pointBlock(iBlock):
    def __init__(self, pt_num: int, x: float, y: float, z:float, o:float, a:float, t:float, p1:float, p2:float):
        super().__init__()
        self.pt_num = pt_num
        self.x = x
        self.y = y
        self.z = z
        self.o = o
        self.a = a
        ...
```
Группируем данные по смыслув простейшие `NamedTuple`  -- и иммутабельные, и быстро пишется (автор питоновского  `NamedTuple` явно любил лисп:).
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

## 4. Странные решения: дублирование методов
Излишний функционал
```
class Graph:
    # предусловие: на входе действительно подмножество
    def reject(self, id_subset:set[int]):
        ...

    # предусловие: на входе действительно подмножество
    def subgraph(self, id_subset:set[int]) -> Graph:
        if ...:
            self._c_status = Statue.ERR
           return None
        return deepcopy(self).reject(id_subset)
```

Наверное, все же, следовало бы оставить только `subgraph`, он не меняет внутреннее состояние основного объекта, а при большом желании делать присваивание. Убираем `reject`:
```
from __future__ import annotations
class Graph:
	...   
    def subgraph(self, id_set:set[int]) -> Graph:
        ans = deepcopy(self)
        ...
        # все что было внутри старого reject
        ...
        return ans
```

## 5. Чрезмерный результат
Из некритичного, у меня есть чрезмерный результат, заложенный на будущее -- помимо самих координат хранятся индексы отрезков, которые змейка пересекла:

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
