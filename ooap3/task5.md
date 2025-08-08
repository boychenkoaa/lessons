## Решение задания 5

Еще немного колдуем
- `Session` -- фасад над
    - `IO` -- класс с операциями `get` и `put`, фасад над
        - `InputParser` -- парсит вводную строку и делает сериализацию команды 
        - стандартным вводом-выводом
    - `Game` -- фасад над
        - `Cells`
        - `Statistics`
        - основной метод -- `Transform`
          
- `CellsFabric` --  генератор начального состояния ячеек
- `GameCommand` -- вычисляет `GameTransformation`
(фасад над  `CellsTransfomration` и `StatisticsTransfomtation`)
