## Описание работы
1. Сегодняшний подопытный -- функции добавления в Компас двумерной геометрии через его API. (Классы ksEditor  и его наследники) [editor2d.py](editor2d.py)
2. Пришлось добавить и классы-обертки для геометрии, и для элементарных преобразований линейной алгебры [geom_raw.py](geom_raw.py)
3. В целом сделал вывод что нужно просто продублировать у себя классы Компасовских примитивов, добавив к ним нужный мне функционал.
4. Иерархию нужно организовывать так же как и в Компасе -- чтобы не держать в голове две иерархии. (возможны упрощения, но не другая структура, подчиненность должна сохраняться, названия быть похожи)
5. Тесты сделаны элементарные, но с заделом на модификацию под фаззинг [editor2d_test.py](editor2d_test.py).

## Общие впечатления.
1. Задание далось с изрядными трудностями, как будто учишься писать левой рукой.
2. Сосредоточение только на "хотелках" потянули за собой каскадно изменения всего проекта, ревизию всех модулей, кроме GUI. 
Когда голова не забита деталями реализации, сразу же понятно, что должно быть публичным а что приватным, какие нужны вспомогательные классы и вспомогательные типы. Паззл складывается гораздо бодрее, чем при "итеративном" думании, но при этом кусочки нового пазла несовместимы со старым. А вот внутреннее наполнение брать можно и нужно.
3. В итоге, в результате вместо тестирования одного класса я написал интерфейсы для двух третей проэкта (и то остановился чисто из-за сроков). Я хотел бы довести идею до конца, переписать таким образом проэкт и посмотреть еще на подводные камни, но тогда я выйду вообще за все разумные сроки в задании, а в работе я продолжу, да). 

## Выводы.
1. Спецификация существует у меня в голове и, возможно, раскидана по комментариям. Как-то словесно она не описывается, что плохо. Что с этим делать, пока непонятно (наверное, будет на следующих уроках...).
2. Тесты частично ее формализуют (реализуют, представляют), где-то избыточно, где-то недостаточно. Тесты != спецификация. Тесты это все равно, в конечном счете, код.
4. Степень соответствия тестов и спецификации остается на моей совести и моей ответственности как разработчика.
6. При реализации могут всплыть косяки и неточности в спецификации, что влечет за собой челночный бег между тестами и реализацией. Это плохо, но неизбежно, тут только опыт решает. 
7. Даже с учетом вышеизложенного получается строже и надежнее, чем "итеративным" подходом. 
8. Как вариант раздавать таким образом задачи джуниорам: я пишу базовые тесты, они наполняют классы, добавляют свои тесты при необходимости, и фаззинг в самом конце, дополняя через это соответствие тестов спецификации, я рефакторю.

