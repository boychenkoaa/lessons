# Исправленное решение

**Вариация**
- неудачное (но "интуитивно" (с точки зрения геометрии) напрашивающееся) наследование
- а вообще, нужна композиция либо обобщение класса GeomGraph

```python
from typing import TypeVar, Generic

# Пример 1: вариация
class GeomGraph:
    def find_point(x, y) -> int:
        ...
        
    def get_point(id_: int) -> Point2:
        ...
    
    def add_point(x, y) -> None:
        ...
        
    def remove_point(x, y) -> None:
        ...
        
    def remove_point_by_id(id: int) -> None:
        ...
     
class Polygon(GeomGraph):
    # вариация типа
    def add_point(x, y, contour_index, prev_index):
        '''
        добавление точки в полигон требует также добавления двух новых ребер, 
        удаления одного старого
        и проверки на самопересечения
        '''
        ...
        
    # вариация функциональная
    def remove_point(x, y):
        '''удаление в полигоне требует не просто удаления точки из контейнера
        но и создания нового ребра между новыми соседями
        а еще проверки на отсутствие самопересечения
        '''
        ...

```

**Конкретизация**
```python
T = TypeVar("T")
class BSTree(Generic[T]):
    def find(self, key: int) -> T:
        ...
        
    def add(self, key: int, value: T):
        ...
        
    def remove(self, key: int):
        ...
        
class AVLTree(BSTree[T]):
    def find(self, key: int) -> T:
        # тут уже конкретные реализации
        ...
        
    def add(self, key: int, value: T):
        # тут уже конкретные реализации
        ...
        
    def remove(self, key: int):
        # тут уже конкретные реализации
        ...
```

**Структурное наследование**
Примеси
```python
# примесь для печати в матплотлибе
class PlotMixin:
    @property
    def segments(self) -> list[Segment2]:
        raise NotImplementedError()
          
    def plot(self, plt, **kwargs):
        for segment in segments:
            plt.plot([segment[B][X], segment[E][X]],[segment[B][Y], segment[E], [Y]], **kwagrs)

# абстрактная геометрия
class Geometry2D:
    ...
    @property
    def segments(self):
        raise NotImplementedError()


# пример
# plot доступен автоматически
class ProjectPline2D(Geometry2D, ToMeshMixin, PlotMixin):
    def segments(self):
        return list(zip(self.points, self.points[1:]))
```

# Неверное решение
Невнимательно прочитал задание, сделал просто словесное описание, сегодня исправлю, доделаю примеры кода

**Вариация - 1**
Плохая реализация: наследуем поверхность от плоскости с переопределением методов получение уравнение, получить точку и т д

**Вариация - 2**
Допустимым кажется переопределение __str__ (и особенно __repr__) у потомков -- при выводе на печать важно видеть, что "пробрался" частично определенный класс

**Наследование с конкретизацией - 1**
Класс ДеревоПоиска (частично реализованный) и его наследники АВЛДерево и КрасноЧерноеДерево

**Наследование с конкретизацией - 2**
Годот: класс PhysicsBody2D (абстрактный) и его наследники CharacterBody2D, RigidBody2D, StaticBody2D уже реализуют конкретное поведение

**Структурное наследование - 1**
Примеси (например, `LoggerMixin`)

**Структурное наследование - 2**
в Годоте есть базовый класс RefCounted (который просто гарантирует уникальность айди при создании класса) и почти все, что может быть в сцене, унаследовано от него -- но при этом выходит далеко за пределы его функционала
