# Урок 1. Цикломатическая сложность

## Пример 1
Вводные
- Я не оптимизирую "вычислительную" часть
- Лечим метод `point_check`

Файлы
- до [example1.py](example1.py) , ЦС = 17
- после [example1_done.py](example1_done.py) ЦС = 2

Проделан рефакторинг:
- Первые два параметра используются только вместе -- заменяем на один
- `flag` увеличивается на 1 вместе с добавлением элементов в массивы. Во первых это не флаг тогда, а во вторых всегда флаг=сумме длин массивов -- дублирование состояния без особых на то причин. Убираем эту переменную
- Переименовал функцию и некоторые переменные на более наглядные имена

Снижаем ЦС:
- Три повторения одного и того же цикла по одному шаблону выделил в отдельную функцию `find_used_edges`
- В этой функции используются ФП-фишки
- Внутри `while` `if` не нужен -- это проход по всем и последующая очистка
- Внутри for он не нужен тоже, можно сделать `filter`

## Пример 2

Вводные
- `Status.update_y` - наш сегодняшний пациент
- Он избыточно сложен
- Метода лечения два -- упрощение условий и использование полиморфизма

Файлы
- до [example2.py](example2.py) ЦС = 12
- после [example2_done.py](example2_done.py) ЦС = 1

Снижаем ЦС:
- Классы `Edge` можно сравнивать двумя способами. Первый способ стандарнтый - как пару кортежей `(x1,y1),(x2,y2)`Второй способ -- "сравнение в статусе", более специфичен для реализуемого алгоритма (находится внутри старого while)
- Чтобы бинарный поиск (точнее -- бисекция!) работала корректно, я просто сделаю наследника от `Edge` -- `StatusEdge` с переопределенным методом `__le__` и декоратором `@total_ordering`
- Если вдруг припечет, то для `StatusEdge` можно явно вызвать и стандартное сравнение, удобно
- Cравнение в статусе я не удержался и тоже переписал не просто избавлением от `else`, но и упрощением самих вычислений. В этом задании такое не приветствуется (нужно менять форму не меняя содержания), но когда я могу заменить пять сложных условий на два простых, мне сложно пройти мимо.

## Пример 3
Вводные
- препарируем метод `nearest_geom_connection`
- табличный метод позволил избавиться сразу от всего

Файлы
- до [example3.py](example3.py) ЦС = 12
- после [example3_done.py](example3_done.py) ЦС = 1
  
Снижаем ЦС
- табличная логика - простое перечисление вариантов в таблице -- помогла снизить ЦС до 1
- можно было бы сделать перечисление через декартово произведение, но мне это видится уже выхолащиванием...
еще можно было бы вытащить эту таблицу наружу -- но тогда пришлось бы внутри метода городить еще один словарь типа {"EH": EH, "ET": ET} что мне в данном примере тоже видится выхолащиванием, да и снаружи эта таблица как таковая пока не особо нужна
- но, справедливости ради, тестировать все равно нужно все случаи в таблице
- стало покороче и поменьше условий

## Выводы 
1. До НГ ставлю себе задачу ввести метрику измерение ЦС вновь добавляемого кода.
2. При код-ревью обязательно буду автоматически измерять ЦС (настрою CI/CD), если превышает 10-15 -- это будет повод поговорить.
3. ЦС можно уменьшить, не вникая в сами вычисления (преобразования), а только лишь отслеживая логику исполнения, хотя удобнее конечно по возможности видеть картину целиком.
