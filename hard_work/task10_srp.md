# Задание 10
Задание: 5-7 строк нарушающих SRP

Сегодня правим небольшую прогу которая считает траектории на поверхностях вращения

## 1. 
Было (надо давно поправить код, когда я не знал как распаковывать словари)
```
traj_props = TrajectoryProperties(rx=settings["rx"], ry=settings["ry"], rz=settings["rz"], p1=math.radians(settings["p1_deg"]), h_safe=settings["h_safe"], v_free=settings["v_free"], vj_free=vj_free)
```
Стало
```
settings["p1"] = math.radians(settings["p1"])
traj_props = TrajectoryProperties(**settings, vj_free=vj_free)
```
## 2. 
Было: три лямбда-функции в параметрах
```
cone = ConeSpiral(H=H, generatrix_f0=lambda x: (R1 - R0) / H * x + R0, derivative_gf0= lambda x: (R1 - R0) / H, spiral_step=settings["delta"], err_f = lambda phi: 6 * cos(phi-pi / 3.0))
```

исправляем (проблема не только в этой строке, но она прямо запутанная)
вводим доп. классы

```
class RotationSurface:
    def generatrix(self, x: float) -> float:
        ...

    def derivative(self, x: float) -> float:
        ...

    def R(self, x: float) -> float:
        ...

class ConusSurface(RotationSurface):
    def __init__(self, R1: float, R0: float, H: float):
        self._R1 = R1
        self._R0 = R0
        self._H = H

    @property
    def R0(self) -> float:
        return self._R0

    @property
    def R1(self) -> float:
        return self._R1

    @property
    def H(self) -> float:
        return self._H

    def R(self, x: float) -> float:
        return (self.R1 - self.R0) / self.H * x + self.R0

    def derivative(self, x: float) -> float:
        return (self.R1 - self.R0) / self.H 

class ExcentricConusSurface(ConusSurface):
    def __init__(self, R1: float, R0: float, H : float, R_shift: float, start_angle: float):
        super().__init(R0, R1, H)
        self._R_shift = R_shift
        self._start_angle = start_angle
        
    def _R_correction(angle: float) -> float:
         return math.cos(angle - self._start_angle)*self._R_shift

    def R(self, angle: float, x: float) -> float:
        return super().R(angle, x) + self._R_correction(angle)


class Spiral:
    def __init__(self, rotation_surface: RotationSurface, delta: float, start_angles: list[float] = []):
        ...
```

стало - итог
теперь смотрится аккуратно, и внутри не идеально, но для этой задачи достаточно

```
shifted_conus = ExcentricConusSurface(R1, R0, H, 6, math.pi/6)
spiral = Spiral(surface = shifted_conus, delta = 40, start_angles = [0, math.pi])
```

## 3. 

было -- еще один перебор
эта строчка приведена чтобы показать что xyz_list тоже слеплен из частей, которые потом раскрываются
```
xyz_list =  [(x(p), 0, f(x(p), h)) for p in angles]
# проблемная строка
ans = [yPoint(xyz_list[i][X], xyz_list[i][Y], xyz_list[i][Z], props.rx, props.ry, props.rz, props.p1, xi_list[i], v_list[i], vj_list[i]) for i in range(N)]
```

исправляем
```
x_list = list(map(x, angles))
z_list = list(map(f, x_list))
rx, ry, rz = props.rx, props.ry, props.rz
```

стало
```
ans = [yPoint(x, 0, z, rx, ry, rz, xi, v, vj) for x, z, xi, v, vj in zip(x_list, z_list, xi_list, v_list, vj_list)]
```

## 4. 
Перебор с множественным присваиванием

было
```
x, a, H, F, h, u, delta = self._cone.x, self._cone.a, self._cone.H, self._cone.F, self._h, self._u, self._cone.delta
```

стало
разбиваем по назначению и смыслу, первые 4 это размеры, F - функция, h, u -- не относятся к конусу
```
x, a, H, delta = self._cone.x, self._cone.a, self._cone.H, , self._cone.delta
F = self._cone.F
h, u = self._h, self._u
```

## 5. 
Было: строчка разрослась из за обращения к координатам
```
def polygonize_dr_objects(...):
    ...
    return [[list(shapely_polygon.exterior.coords)] + [list(interior.coords) for interior in shapely_polygon.interiors] for shapely_polygon in shapely_polygons]
```

Стало: 
```
# вводим новую функцию
def contours_of_polygon(polygon: Polygon):
    return [polygon.exterior] + list(polygon.interiors)

# вторая укорачивается
def polygonize_dr_objects(...):
    return [contour.coords for contous in contours_of_polygon(shapely_polygon)]
```

## 6
Не совсем по теме, но читаемость повышается

Было
```
string_list = [head1_str] + points1_str_list + [head2_str] + points2_str_list + [inst_str, dout_str] + traj_str_list + [end_str]
```
Стало (не поменялось вообще ничего, кроме читаемости)). Программа для робота составляется из блоков легче воспринимается именно в таком порядке.
```
string_list = [head1_str] + \
    points1_str_list + \
    [head2_str] + \
    points2_str_list + \
    [inst_str] + \
    [dout_str] + \
    traj_str_list + \
    [end_str]
```


## Общий вывод
Чрезмерно длинные строки затрудняют восприятие и провоцирует ошибки. Умеренное разбиение строки устраняет эту проблему.
