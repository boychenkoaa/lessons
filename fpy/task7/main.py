from __future__ import annotations
from typing import Callable, NamedTuple

from pymonad.list import ListMonad
from pymonad.maybe import Maybe, Just, Nothing

RC = NamedTuple('RC', [('r', int), ('c', int)])

"""
вспомогательные классы
SimResult -- хранит все состояние -- список клеток, размеры поля, номер дня

общая идея: монада Maybe

главная функция -- sim
берет board
вызывает step(board)
если получился Nothing (конец рекурсии) - возвращает result
если получился new_board != Nothing, вызывает sim(new_board)

step вычисляет новую доску либо Nothing
для печати step вызывает коллбэк after_step

сейчас для простоты каждый раз заново пересчитывается вся доска
занимает O(steps * M * N) по времени
можно оптимизировать, чтобы обсчитывались только граница (= вновь добавленные ячейки)
но не в этот раз...
"""

# базовый класс, иммутабельный
class Board(NamedTuple):
    cells: frozenset[RC]
    m: int
    n: int
    day: int

    # тут map уже больше шутка чем необходимость)
    def __repr__(self):
        return f'день {self.day}\n' + '\n'.join(
            map(lambda r: ' '.join(
                map(lambda c: '1' if RC(r, c) in self.cells else '0', range(self.n))
            ), range(self.m))
        ) + '\n'

    def is_final(self) -> bool:
        return len(self.cells) == self.m * self.n


_DIRECTIONS = (RC(-1, 0), RC(1, 0), RC(0, -1), RC(0, 1))

# корректных соседей по полю ищем аналогично с задачей про коня
# фильтр
def is_valid(rc: RC, r: Board) -> ListMonad:
    return ListMonad(rc) if 0 <= rc.r < r.m and 0 <= rc.c < r.n else ListMonad()

# генерация соседей и фильтрация
def _nb(rc: RC, r: Board) -> ListMonad:
    return (
        ListMonad(*_DIRECTIONS)
        .map(lambda d: RC(rc.r + d.r, rc.c + d.c))
        .bind(lambda p: is_valid(p, r))
    )


# само вычисление следующей доски
def calculate(board: Board, after_step: Callable[[Board], None]) -> Maybe:
    expanded = frozenset(
        ListMonad(*board.cells).bind(lambda rc: _nb(rc, board))
    )
    new_board = Board(board.cells | expanded, board.m, board.n, board.day + 1)
    after_step(new_board)
    return Just(new_board)


# основной шаг
# если поле заполнено, вернет Nothing
# иначе вычислит новый SimResult обернутый в Just
def step(board: Board, after_step: Callable[[Board], None]) -> Maybe:
    return (
        Nothing if board.is_final() else Just(board)
    ).bind(lambda brd: calculate(brd, after_step))


# рекурсивный процесс симуляции. Обрывается сам при возврате Nothing из step
def sim(board: Board, after_step: Callable[[Board], None]) -> Board:
    return step(board, after_step).maybe(board, lambda new_board: sim(new_board, after_step))


if __name__ == '__main__':
    # возьмем повторяющиеся ячейки
    start = Board(frozenset({RC(2, 2), RC(2, 1), RC(2, 2)}), 5, 5, 0)

    print(f'--- с печатью ---\n{start}\n')
    final = sim(start, after_step=print)
    print(f'потребовалось дней: {final.day}')

    print('\n--- тихий режим ---')
    final = sim(start, after_step=lambda _: None)
    print(f'потребовалось дней: {final.day}')
