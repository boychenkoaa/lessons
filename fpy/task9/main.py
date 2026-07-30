# алгоритм
# список общий => список пар
# список пар - map + лямбда + аккумулятор

from dataclasses import dataclass, replace
from functools import reduce

# общая идея: тащим промежуточное состояние
# нужен только dist, остальное - техническое
# is_v -- является ли скоростью текущий элемент
# v -- предыдущая скорость
# t -- предыдущее время
# само вычисление при этом не меняется, но протаскиваемое состояние явно постулируется
# Наверное это изящно. Но тяжеловесно. Цикл налепить проще :)

@dataclass(frozen=True)
class TmpState:
    dist: int
    is_v: bool
    v: int
    t: int

if __name__ == "__main__":
    oxana = [15, 1, 25, 2, 30, 3, 10, 5]
    dist = reduce(
        lambda tmp, elem:
            replace(tmp, is_v=False, v=elem) if tmp.is_v
            else replace(tmp, dist=tmp.dist + tmp.v * (elem - tmp.t), is_v=True, t=elem),
        oxana,
        TmpState(dist=0, is_v=True, v=0, t=0),
    ).dist
    print(dist)
