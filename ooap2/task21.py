# Льготное наследование
# если агрегаций будет много, можно организовать им свою иерархию и "прокинуть" мост
class GraphIterator(Generic[T]):
    def __init__(self, g: Graph[T]):
        ...
        
    def next(self) -> T:
        ...
        
class DFSGraphIterator(GraphIterator[T]):
    def next(self) -> T:
        # следующий элемент при обходе в глубину
        ...

# льготное наследование -- обход графа мы умеем, навешиваем агрегацию
# правда, отчасти это и наследование реализации
# строго говоря, агрегация не обязана быть коммутативной
class DFSGraphIteratorAggr(DFSGraphIterator[T], Generic[V]):
    def __init__(self, aggregate_function: Callable[[T, V], V], start: V):
        super().__init()
        self._aggr_func = aggregate_function
        self._result = start
        
    def next(self):
        item = super().next()
        self._result = self._aggr_func(item, result)
        return item
    
    def result(self):
        return self._result
        

# Наследование реализации -- класс kdPointContainer и его предки

# абстрактный класс контейнера точек
class PointContainer:
    def get(self, id_: int) -> Point2:
        ...
        
    def set(self, id_: int, point2: Point2):
        ...
    
    def add(self, point2: Point2):
        ...

# абстрактный класс дерева поиска для точек
class PointSearchTree:
    def add(self):
        ...
        
    def find(self, point2: Point2):
        ...
        
class kdTree(PointSearchTree):
    # здесь реализация конкретно кд-дерева
    ...
    
class kdPointContainer(PointContainer, kdTree):
    # наследуем kdTree -- получаем в наследство конкретную реализацию поиска точки за log(N)
    ...
