# Задание 8, решение.
Типизация динамическая, ко- и контра-вариантность только через `typing`

"Игрушечный" пример. Попробовал все 4 варианта.

```python
from dataclasses import dataclass

from typing import TypeVar, Generic


class Point2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"Point2(x={self.x}, y={self.y})"
        
    def __repr__(self):
        return f"Point2(x={self.x}, y={self.y})"

class Point3(Point2):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z
        
    def __str__(self):
        return f"Point3(x={self.x}, y={self.y}, z={self.z})"
    
    def __repr__(self):
        return f"Point3(x={self.x}, y={self.y}, z={self.z})"

T_cov = TypeVar('T_cov', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)

class PointContainerCov(Generic[T_cov]):
    def __init__(self):
        # для простоты
        self._li = []

    def add(self, point: T_cov):
        self._li.append(point)

class PointContainerContra(Generic[T_contra]):
    def __init__(self):
        # для простоты
        self._li = []

    def add(self, point: T_contra):
        self._li.append(point)
        
        
PointContainerContra2 = PointContainerContra[Point2]
PointContainerContra3 = PointContainerContra[Point3]
PointContainerCov2 = PointContainerCov[Point2]
PointContainerCov3 = PointContainerCov[Point3]

def print_container_con2(container: PointContainerContra2):
    print('con2')
    print(type(container))
    for point in container._li:
        print(point)
        
def print_container_cov2(container: PointContainerCov2):
    print('cov2')
    print(type(container))
    for point in container._li:
        print(point)

if __name__ == "__main__":
    p2 = Point2(x=1.0, y=2.0)
    p3 = Point3(x=3.0, y=4.0, z=5.0)
    container_cov2 = PointContainerCov2()
    container_cov3 = PointContainerCov3()
    container_con2 = PointContainerContra2()
    container_con3 = PointContainerContra3()
    container_cov2.add(point=p2)
    container_cov2.add(point=p3)
    container_cov3.add(point=p2)
    container_cov3.add(point=p3)
    container_con2.add(point=p2)
    container_con2.add(point=p3)
    container_con3.add(point=p2)
    container_con3.add(point=p3)
    print_container_con2(container_con2)
    print_container_con2(container_con3)
    print_container_cov2(container_cov2)
    print_container_cov2(container_cov3)
    print('ok')
```
 
Вывод тайп-чекера
>src\main.py:36: error: Cannot use a covariant type variable as a parameter  [misc]
>src\main.py:74: error: Argument "point" to "add" of "PointContainerCov" has incompatible type "Point2"; expected "Point3"  [arg-type]
>src\main.py:78: error: Argument "point" to "add" of "PointContainerContra" has incompatible type "Point2"; expected "Point3"  [arg-type]
>src\main.py:81: error: Argument 1 to "print_container_con2" has incompatible type "PointContainerContra[Point3]"; expected "PointContainerContra[Point2]"  [arg-type]
>Found 4 errors in 1 file (checked 1 source file)
