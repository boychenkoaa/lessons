from math import sqrt
from enum import Enum
from typing import NamedTuple

Point23 = tuple[float, float] | tuple[float, float, float]
PointKey = tuple[int, int] | tuple[int, int, int]

# класс множества точек, с точностью до эпсилон
# эпсилон можно регулировать
# проверка на вхождение точки за O(1) в среднем
# используется при нахождении "висячих" вершин при лечении слоя
# точнее, для классификации вершин на совпадающие и висячие
# совпадающие соединяются отрезками, висячие отмечаются маркерами
# в дальнейшем возможно использование для хранения облаков точек, пришедших со сканера
# также для схожих целей (быстрый поиск дубликатов) можно использовать при "сшивке" слоя, и вообще на всех алгоритмах, которые сшивают "разбросанную" геометирю

class Point2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
    def __getitem__(self, index: int):
        return (self.x, self.y)[index]
    
    def __len__(self):
        return 2
       

class Point23Ext(NamedTuple):
    point: Point23
    ext: int

class Dim23 (Enum):
    DIM2 = 2
    DIM3 = 3

class StrangePoints:
    def __init__(self, epsilon: float, dim: Dim23):
        self._di = {}
        self._epsilon = epsilon
        self._dim = dim
        
    @property
    def dim(self):
        return self._dim
    
    def dist(self, point1: Point23, point2: Point23):
        assert len(point1) == self.dim and len(point2) == self.dim
        return sqrt(sum([(point1[i] - point2[i])**2 for i in range(self.dim)]))
    
    def _eq_d(self, point1: Point23, point2: Point23) -> bool:
        return self.dist(point1, point2) < self.epsilon
    
    def _eq_key(self, point1: Point23, point2: Point23) -> bool:
        return self._key(point1) == self._key(point2)
    
    def _eq(self, point1: Point23, point2: Point23) ->  bool:
        return self._eq_d(point1, point2) or self._eq_key(point1, point2)
    
    @property
    def epsilon(self):
        return self._epsilon
    
    def _approx_x(self, x: float) -> int:
        return round(x / self.epsilon)
    
    def _key(self, point: Point23) -> PointKey:
        return tuple([self._approx_x(x) for x in point])
    
    def _nb_keys(self, key: PointKey) -> set[Point23]:
        ans = [(key[0] + i, key[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
               
        if self.dim == 3:
            ans = [(*rc, key[2] + k) for rc in ans for k in (-1, 0, 1)]
        
        return set(ans)
    
    def nearest_nb(self, point: Point23) -> Point23:
        nb_keys_non_empty = self._nb_keys(self._key(point)).intersection(set(self._di.keys()))
        if not nb_keys_non_empty:
            return None
        min_key = min(nb_keys_non_empty, key = lambda k: self.dist(self._di[k].point, point))
        return self._di[min_key]
    
    # ближайшая только в рамках кругло-квадратной окрестности
    def nearest_pointext(self, point: Point23) -> Point23Ext:
        nearest_pext = self.nearest_nb(point)
        if nearest_pext is None or not self._eq(nearest_pext.point, point):
            return None
        return nearest_pext
        
    def has_point(self, point: Point23) -> bool:
        return self.nearest_pointext(point) is not None
    
    def ext(self, point: Point23):
        nearest_pext = self.nearest_pointext(point)
        if nearest_pext == None:
            return None
        return nearest_pext.ext
    
    # возвращает True если точка была успешно добавлена и False если точка уже есть
    def add(self, point: Point23, ext:int|None = None):
        if self.has_point(point):
            return False
        
        self._di[self._key(point)] = Point23Ext(point,ext)
        return True
      
    # возвращает True если точка была успешно удалена и False если точки не было
    def remove(self, point: Point23) -> bool:
        nearest_pointext = self.nearest_pointext(point)
        if nearest_pointext is None:
            return False
        
        self._di.pop(self._key(nearest_pointext.point), None)
        return True
    
    def __len__(self):
        return len(self._di)