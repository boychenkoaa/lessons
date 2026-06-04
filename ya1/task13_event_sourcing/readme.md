# Задача 13. Event Sourcing

Реализация Event Sourcing, как я его понимаю :-)

Слои:
- [base.py](base.py) - базовый тип-перечисление статуса выполненной команды
- [pure_robot.py](pure_robot.py) - функции базовые робота
- [robot_commands.py](robot_commands.py) - команды-функции-обертки для складывания в историю, возвращают замыкание
- [command_handler.py](command_handler.py) - EventStore и CommandHandler согласно заданию
- [main.py](main.py) - простой тестовый прогон с использованием undo и redo

Комментарий
- Напрашивается еще один слой - `robot_api`. Чтобы в `main` не тянуть импорты из предыдущих слоев. C методами `move`, `turn`, ... , а также `undo`, `redo`. В рамках учебной задачи посчитал избыточным.