## Решение задания 8

### 0. Глобальные константы
```
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
```

список сейчас указан неполный, в нем суммарно 32 комбинации

```
COMBINATION_MASKS = 
{
''T_up": [(-2, 0), (-1, 0), (0,0), (1, 0), (2,0), (0,1), (0,2)],
''T_down": [(-2, 0), (-1, 0), (0,0), (1, 0), (2,0), (0,-1), (0,-2)],
"3h_mid": [(-1, 0), (0, 0), (1, 0)],
"3h_left": [(-2, 0), (-1, 0), (0, 0)],
"3h_right": [(0, 0), (1, 0), (2, 0)],
"3v_mid": [(0, -1), (0, 0), (0, 1)],
"3v_down": [(0, -2), (0, -1), (0, 0)],
"3v_up": [(0, 0), (0, 1), (0, 2)]
}
```
### 1. Базовые типы

### Типы-перечисления
- Bonus - типы бонусов
- Combination - типы комбинаций (см константу COMBINATION_MASKS)
- Stone - типы камней на поле

### Встроенные типы с ограничениями
**АТД BoundedInt** (параметризуется MinVal и MaxVal)

*команды*
- add (other: int) -> BoundedInt
  
*запросы*
- value -> int
- RowInt = BoundedInt(0, BOARD_HEIGHT)
- ColumnInt = BoundedInt(0, BOARD_WIDTH)
- NonNegativeInt = BoundedInt(0, +inf)
- BonusCount = NonNegativeInt

### Типы-алиасы
- RC = Tuple[RowInt, ColumnInt]
- Mask = Tuple[Tuple[int, int]]

### 2. Игровая логика -- низкий уровень. Хранение.

**АТД Cells** -- поле с ячейками

*команды*
- erase_rc(rc: RC)
- update_rc(rc: RC, stone: Stone)

*запросы*
- get_rc(rc) -> CellValue

**АТД Board** -- инкапсулирует логику среднего уровня для доски

*запросы*
- apply_mask(rc, mask: Mask) -> RCSet
- mask_is_full(rc, mask: Mask) -> bool
- find_by_value(cell_value) -> RCSet
- repr() -> str

*команды*
- Swap(rc1, rc2)
- Erase(RCSet)
- EraseByMask(rc, mask)
- FillRandom()
- FillRandomOneLine()
- duplicate(rc: RC,rc_set: RCSet)
- Shuffle
- Drop

**АТД BonusChest**

*запросы*
- bonus_count(bonus: Bonus) -> BonusCount()
- repr() -> str

*команды*
- use_bonus(bonus) (предусловие: бонусов больше одного)
- add_bonus(bonus)
- add(other: BonusChest)

**АТД Statistics**

*запросы*
- scores -> int
- bonus_used_count(bonus: Bonus) -> int
- combinations_used_count(combination: Combination) -> int
- repr()
- 
*команды*
- reset()
- add(statistics: Statistics)

### 3. Игровая логика -- средний / высокий уровень. Шаги и ходы.

**АТД GameSession**
'''фасад над доской, сундуком и статистикой'''

*запросы*
- is_print_on -> bool
- last_step_status -> Status
- possbile_swap_move() 
- possible_bonus_move()

*команды*
- reset()
- print()
- one_auto_step() (предусловие: комбинации есть)
- long_auto_step() (предусловие: комбинации есть)
- bonus_step(bonus: Bonus) (предусловие: есть соответствующий бонус в ящике)
- swap_step(rc1: RC, rc2: RC) (предусловие: обмен возможен)
  
**АТД Game**
'''обертка над GameSession'''

*команды*
- BonusMove(bonus)
- SwapMove(rc1, rc2)
- print()
- exit()
- reset()
- turn_on_print()
- turn_off_print()

*запросы*
- is_print_every_step() -> bool
- possible_moves() -> bool

### 4. Пользовательский интерфейс

**АТД GameUI**

*команда* 
- move(str) (предусловие: строка корректна)

### Примечания
Изначально я сделал решение с иерархией шагов и ходов (step, очевидно, можно превратит). Но тогда это противоречит требованию, что класс не должен делать что-то одно -- видимо в этом задании посетители запрещены. Поэтому получилось в итоге вообще без наследования и иерархий.
