'''
Задание 12. Попытка присваивания.
У меня получилось, что Any не нужндается в переопределении попытки присваивания, и ее можно сделать "финальной" в General
"конструктора копирования" в Python нет
'''

class General:
    ...
  
    @final
    @classmethod
    def try_set(cls, other) -> _T:
        if isinstance(other, cls):
            return other

        return Void


class Any(General):
    ...

class MyNone(Any):
    ...

Void = MyNone()

# тестируем
if __name__ == '__main__':
    # при попытке присваивания копируется ссылка либо возвращается None
    g = General()
    a = Any()
    g = g.try_set(a)
    assert a == g
    assert a is g

    # неприводимые типы
    g = General()
    a = Any()
    a = a.try_set(g)
    assert a == Void

    # еще одни неприводимые типы
    a = Any()
    a = a.try_set(1)
    assert a == Void
