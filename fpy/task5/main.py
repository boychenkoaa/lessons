from pymonad.maybe import Just, Maybe, Nothing
from pymonad.tools import curry

# посадка птиц на левую сторону
to_left = lambda num: (
    lambda s: Nothing if abs((s[0] + num) - s[1]) > 4 else Just((s[0] + num, s[1]))
)

# посадка птиц на правую сторону
to_right = lambda num: (
    lambda s: Nothing if abs((s[1] + num) - s[0]) > 4 else Just((s[0], s[1] + num))
)

# банановая кожура
banana = lambda _: Nothing


# отображение результата
# тут исправил на случае Nothing, чтобы не обращался к Value
def show(maybe: Maybe):
    if maybe.is_just():
        l, r = maybe.value
        print(f"OK: left={l}, right={r}")
    else:
        print("Упал!")


if __name__ == "__main__":
    # начальное состояние
    begin = Just((0, 0))

    show(
        begin.bind(to_left(2))
        .bind(to_right(5))
        .bind(to_left(-2))  # канатоходец упадёт тут
    )
    show(
        begin.bind(to_left(2))
        .bind(to_right(5))
        .bind(to_left(-1))  # в данном случае всё ок
    )
    show(
        begin.bind(to_left(2))
        .bind(banana)  # кожура всё испортит
        .bind(to_right(5))
        .bind(to_left(-1))
    )
