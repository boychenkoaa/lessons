Сужение и расширение одновременно

```python
class Quaternion:
    def __init__(self, x: float, y: float, z: float, w: float):
        self._x, self._y, self._z, self._w = x, y, z, w

class NonZeroQuaternion(Quaternion):
    # сужение
    def __init__(self, , x: float, y: float, z: float, w: float):
        super().__init__(x, y, z , w)
        if self.R < self.epsilon:
            self._status = Status.ERR

    @property
    def R(self):
        return (x**2+y*2+z**2+w**2)**0.5

    # и связаное с ним расширение
    def to_euler_angles(self):
        phi = math.atan2(...)
        theta = math.atan2(...)
        psi = math.atan2(...)

```
