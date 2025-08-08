## Решение задания 5

Еще немного колдуем
- `Session` -- фасад над:
    - `IO` -- класс с операциями `get` и `put`, фасад над
        - `InputParser` -- парсит вводную строку и делает сериализацию команды 
        - стандартным вводом-выводом
    - `Game` -- фасад над
        - `Cells` (игровое поле)
        - `Statistics` (статистика)
        - основной метод -- `Transform` (состоит из  `CellsTransfomration` и `StatisticsTransfomtation`)
          
- `CellsFabric` --  генератор начального состояния ячеек
- `GameTransfomationCalculator` -- вычисляет `GameTransformation` по параметрам хода
- `Command` -- описание желаемого действия
(фасад над  `CellsTransfomration` и `StatisticsTransfomtation`)
