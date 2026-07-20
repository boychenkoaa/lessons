from pymonad.tools import curry
from pymonad.maybe import Maybe, Just, Nothing
from pymonad.list import ListMonad

"""
Очень красивая идея, класс, и хорошо дружит с утиной типизацией.
"""

@curry(2)
def add(x, y):
    return x + y

def add10(x):
    return x.map(add(10))


if __name__ == "__main__":
    j = Just(5)
    li = ListMonad(1, 2, 3)
    nth = Nothing

    # применяем
    new_j = add10(Just(5))
    new_li = add10(ListMonad(1, 2, 3))
    new_nth = add10(Nothing)

    # вывод + проверка на совпадение типов
    print(j, type(j))               # Just 5 <class 'pymonad.maybe.Maybe'>
    print(new_j, type(new_j))       # Just 15 <class 'pymonad.maybe.Maybe'>
    print(li, type(li))             # [1, 2, 3] <class 'pymonad.list._List'>
    print(new_li, type(new_li))     # [11, 12, 13] <class 'pymonad.list._List'>
    print(nth, type(nth))           # Nothing <class 'pymonad.maybe.Maybe'>
    print(new_nth, type(new_nth))   # Nothing <class 'pymonad.maybe.Maybe'>
