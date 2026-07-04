# 18. Capability

Общие замечания
- изучил, что такое `Capability`-монада, очень красивая идея. И `Either` заодно.
- вместо состояния теперь "проталкивается" `Capability`
- за основу взят код из задания 11 "монады"

Изменения:
- класс `Capability` и функция `unavailable`, которая возвращается если в текущем состоянии требуемая недоступна
- `CapabilityBuilder`, который возвращает `Capability` в соответствии с `RobotState` и доменными ограничениями
- в сам `pure_robot` добавились функции `can_move`, `can_turn` — это, на мой взгляд, его прерогатива

Дальнейшее расширение:
- Можно комбинировать `Capability` с `Either`, но туда я уже не пошел

Слои
- [`pure_robot.py`](pure_robot.py): базовые типы и перечисления `move`, `turn`, `set_state` и `can_move`, `can_turn`, ...
- [`robot_api.py`](robot_api.py):
- - `unavailable`, `Capability` и его билдер
- - "монадные" обертки: `move_cmd`, `turn_cmd`, ...
- - `init`, `bind` и `pipe`
- [main.py](main.py): smoke-тест на ошибку при невозможной команде
