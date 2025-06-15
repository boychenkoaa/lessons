from __future__ import annotations
from typing import override
from task_14 import Additive, Vector

class AdditiveInt(Additive):
    def __init__(self, value: int):
        self._value = value
        
    @override
    def __add__(self, other: AdditiveInt):
        return AdditiveInt(self._value + other._value)
    
    @override
    def __radd__(self, other: AdditiveInt):
        return self.__add__(other)

    @property
    def value(self):
        return self._value

VecAdd = Vector[AdditiveInt]
Vec2 = Vector[VecAdd]
Vec3 = Vector[Vec2]
AI = AdditiveInt

def test_vector():
    vec = Vector[AdditiveInt]()
    vec.append(AI(1))
    vec.append(AI(2))
    vec.append(AI(3))
    assert vec[0].value == 1
    assert vec[1].value == 2
    assert vec[2].value == 3
    
def test_vector_add():
    vec = Vector[AdditiveInt]()
    vec.append(AI(1))
    vec.append(AI(2))
    vec.append(AI(3))
    vec2 = Vector[AdditiveInt]()
    vec2.append(AI(4))
    vec2.append(AI(5))
    vec2.append(AI(6))
    vec3 = vec + vec2
    assert vec3[0].value == 5
    assert vec3[1].value == 7
    assert vec3[2].value == 9

def test_vec3():
    vec3 = Vec3()
    vec3.append(Vec2())
    vec3.append(Vec2())
    vec3[0].append(VecAdd())
    vec3[0].append(VecAdd())
    vec3[0][0].append(AI(1))
    vec3[0][0].append(AI(2))
    vec3[0][1].append(AI(3))
    vec3[0][1].append(AI(4))
    vec3[1].append(VecAdd())
    vec3[1].append(VecAdd())
    vec3[1][0].append(AI(5))
    vec3[1][0].append(AI(6))
    vec3[1][1].append(AI(7))
    vec3[1][1].append(AI(8))
    assert vec3[0][0][0].value == 1
    assert vec3[0][0][1].value == 2
    assert vec3[0][1][0].value == 3
    assert vec3[0][1][1].value == 4
    assert vec3[1][0][0].value == 5
    assert vec3[1][0][1].value == 6
    assert vec3[1][1][0].value == 7
    assert vec3[1][1][1].value == 8
    vec3_sum = vec3 + vec3
    assert vec3_sum[0][0][0].value == 2
    assert vec3_sum[0][0][1].value == 4
    assert vec3_sum[0][1][0].value == 6
    assert vec3_sum[0][1][1].value == 8
    assert vec3_sum[1][0][0].value == 10
    assert vec3_sum[1][0][1].value == 12
    assert vec3_sum[1][1][0].value == 14
    assert vec3_sum[1][1][1].value == 16

    
if __name__ == '__main__':
    test_vector()
    test_vector_add()
    test_vec3()
    print('ok')
