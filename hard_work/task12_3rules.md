## Пример 1
Эволюция: стандартные типы данных => простейшие алиасы => простые обертки с нарушениями правил => правильно спроектированный класс

Рассматривается класс полилинии

Требования
  1. Может быть размерности 2 и 3  (4х и более мерные не рассматриваем, мы пишем САПР а не реализацию линейной алгебры)
2. Не позволять (хотя бы на уровне аннотаций типов) добавлять в нее точки не той размерности  
3. Полилиния не может быть менее чем из двух точек  
  
**Было**: минималистичное решение: алиасы стандартных типов 
```Python
Point2 = tuple[float, float]  
Pline2 = list[Point2]  
Point3 = tuple[float, float, float]  
Pline3 = list[Point3]  
Pline23 = Pline2 | Pline3  
```

как времянка на коленке за 2 минуты -- отличное решение, лучше чем просто "голые" списки  
  
**Было**: Класс с нарушениями правил (просто обертка над списком):  
```Python
class Pline:  
	def __init__(self, dim: int):  
		self._li = []  
		self._dim = dim  
  
	def append(self, p: Point2 | Point3):  
		self._li.append(p)  
  
	def pop(self, i: index):  
		self._li.pop(i)  
```
косяк 1: нет ограничения на размерность (мне заведомо не нужны четырехмерные полилинии)  
косяк 2: нет ограничений на тип точки (можно сделать винегрет из точек 2-3, либо проверять уже на уровне реализации)  
косяк 3: при удалении нет проверки на корректность индекса  
косяк 4: при удалении нет проверки на то, останется 1 или 0 точек  
  
Что ж, класс используется часто -- сделаем его правильно  
Разделим на два класса -- несмотря на почти полное совпадение, двумерные и трехмерные объекты в нашем случае это очень разные сущности

**Стало**
```Python
class Status(Enum):
	NIL = 0
	OK = 1
	ERR = 2

class Pline2:  
	def __init__(self, dim: int):  
		self._li = []  
		self._pop_status = Status.NIL
		self._insert_status = Status.NIL
		self._dim = dim  
	  

	def __len__(self):
		return len(self._li)

	# добавление в конец	
	def append(self, p: Point2):  
		self._li.append(p)

	# вставка элемента на место i
	# предусловие -- корректный индекс
	def insert(self, index: int, p: Point2):
		if not (0 <= index < len(self._li)):
			self._insert_status = Status.ERR
			return
		self._li.insert(p, index)
		self._insert_status = Status.OK

	# предусловие -- корректный индекс
	# предусловие -- длина не должна стать меньше 2х
	def pop(self, index: int):  
		if not (0 <= index < len(self._li)) or len(self) <= 2:
			self._pop_status = Status.ERR
		self._li.pop(index)
		self._pop_status = Status.OK

```

(аналогичный класс делается для `Pline3` -- это тот случай, когда дублирование не страшно)

Вывод: 
- это, конечно, дольше чем `Pline2 = list[tuple[float, float]]`
- надежность выше однозначно -- нет переходов в недопустимые состояния (разве что явное предупреждение об ошибке) (так и в примере с шахматами корректность хода определяется не только лишь автоматическим выбором цвета.)

*далее будут более банальные примеры*
## Пример 2 (страховка от некорректного внутреннего состояния) 

я понимаю, что класс несколько громоздкий, но не очень понимаю как сделать его проще

<details>
<summary>Много кода</summary>

```Python
from geom2d_base import * 
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")
VALIDATION_OK = "OK"

class AlgoArgument(Generic[T]):
    def __init__(self, name: str, description: str):
        self._name = name
        self._description = description
        self._last_validation_result = ""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description    
    
    def _validate_val(self, value: T):
        ...
    
    def base_type(self):
        return T
    
    def validate(self, value: T):
        self._validate_type(value)
        if self._last_validation_result != VALIDATION_OK:
            return
        
        self._validate_val(value)
        if self._last_validation_result != VALIDATION_OK:
            return
        
        self._last_validation_result = VALIDATION_OK
    
    def _validate_type(self, value: T) -> bool:
        if not type(value) == T:
            self._last_validation_result = "Argument type mismatch"
        self._last_validation_result = VALIDATION_OK
    
    @property
    def last_validation_result(self) -> str:
        return self._last_validation_result
    
    def is_valid(self, value: T) -> bool:
        self.validate(value)
        return self.last_validation_result == VALIDATION_OK

    
class AlgoSpecification:
    def __init__(self, args: list[AlgoArgument], description: str = ""):
        self._di = {}
        self._last_validation_result = ""
        self._description = description
        for arg in args:
            self._di[arg.name] = arg
    
    @property
    def last_validation_result(self) -> str:
        return self._last_validation_result    
    
    # валидация одного параметра
    def _validate_parameter(self, name: str, value):
        arg = self._di.get(name)
        if arg == None:
            self._last_validation_result = "Unknown parameter \'" + name + "\'"
            return
        arg.validate(value)
        if arg.last_validation_result != VALIDATION_OK:
            self._last_validation_result = "Invalid parameter " + name + "\n" + arg.last_validation_result
            return    
        self._last_validation_result = VALIDATION_OK
    
    # чисто механически прогоняем валидацию всех параметров
    def _validate_parameters_by_one(self, params_dict: dict):
        for name, value in params_dict.items():
            self._validate_parameter(name, value)
            if self._last_validation_result != VALIDATION_OK:
                return
        self._last_validation_result = VALIDATION_OK
    
    # валидация параметров в совокупности 
    def _validate_ex(self, params_dict: dict):
        ...
            
    def validate(self, params_dict):
        self._validate_parameters_by_one(params_dict)
        if self._last_validation_result != VALIDATION_OK:
            return
        
        self._validate_ex(params_dict)
        if self._last_validation_result != VALIDATION_OK:
            return
        self._last_validation_result = VALIDATION_OK
        

class NonExAlgoSpecification(AlgoSpecification):
    def _validate_ex(self, params_dict: dict):
        self._last_validation_result = VALIDATION_OK
```
</details>

Я сделал целый класс АТД спецификации геометрического алгоритма, который валидирует пришедший на вход словарь. Сначала почленно (через классы для аргументов, а потом (через определение в потомках) и явно может проверять несовместные состояния (например, нас устраивают только точки из первой четверти)

Цель -- избежать ошибок при "оборачивании" в алгоритмов при расшифровке JSON-ов

Плюсы - универсальность и гибкость
Минусы -- громоздкость, наверняка можно проще сделать то же самое

Пример использования (из тестов)
```Python
class PositiveIntAlgoArgument(AlgoArgument[int]):
    def _validate_val(self, value: int):
        if value <= 0:
            self._last_validation_result = "Value is negative"
            return
        self._last_validation_result = VALIDATION_OK
        
class NegativeFloatAlgoArgument(AlgoArgument[float]):
    def _validate_val(self, value: float):
        if value > 0:
            self._last_validation_result = "Value is positive"
            return
        self._last_validation_result = VALIDATION_OK
    
class aaaStrAlgoArgument(AlgoArgument[str]):
    def _validate_val(self, value: float):
        if value != "aaa":
            self._last_validation_result = "Value is not \'aaa\'"
            return
        self._last_validation_result = VALIDATION_OK
    
class StrangeAlgoSpecification(AlgoSpecification):
    def _validate_ex(self, params_dict: dict):
        if params_dict["a"] % 2 == 0 and params_dict["b"] % 2 == 0:
            self._last_validation_result = "a and b are both even"
            return
        self._last_validation_result = VALIDATION_OK
```

## Пример №3. Конструктор по умолчанию
Моя любимая змейка, которую я хотел уже оставить в покое
Я не придавал этой ошибке большого значения, но все же поправим

**Было**
```python
class Raster:
    def __init__(self):
        self._is_dash_line = False
        self._segments = []      
        
...
    
    def from_beads(self, beads: Beads):
        self._is_dash_line = True
        beads.sort_points()
        self._segments = list(zip(beads.raster_points[::2], beads.raster_points[1::2]))
```

**Стало**
```python
class Raster:
    def __init__(self, beads: Beads):
        self._is_dash_line = False
        self.from_beads(beads)
	...
    
    def from_beads(self, beads: Beads):
        self._is_dash_line = True
        beads.sort_points()
        self._segments = list(zip(beads.raster_points[::2], beads.raster_points[1::2]))
```


**Что поправил**: добавил конструктор по умолчанию нормльный

## Пример 4 (неполный конструктор по умолчанию)

**Было**
```Python
class DCEL:
	def __init__(self):
		self._base_graph = Graph()
```

граф заполняется неизвестно где, надо дать на вход в конструктор
конечно надо давать граф сразу на вход в конструктор

**Стало**
```Python
class DCEL:
	def __init__(self, base_graph: Graph):
		self._base_graph = copy(base_graph)
```

	
## Пример 5: простые типы данных
 **Было:** 
 делал наспех -- для алгоритма на графе анализ топологии возвращал строку

```python

def connected_graph_topology_type(connected_graph: BiGraph) -> str:
    ...
    
    return "GG"
```

**Стало:**
поправил, возвращает перечисление

```python
class ConnectedGraphTopologyType(Enum):
    TopologyGG = 0
    TopologyPline = 1
    TopologyContour = 2
    TopologyPoint = 3
    TopologySegment = 4
    TopologyTree = 5
    
CGTT = ConnectedGraphTopologyType

...

def connected_graph_topology_type(connected_graph: BiGraph) -> CGTT:
    ...
    
    return CGTT.TopologyGG
```

## Пример 6
Снова типовая ошибка, при спешке не сделал перечисление
**Было**
```python
class Doc2:
	def selection2d_by_types(self, types: list[int]):
		...

```

**Стало** (дублируем файл компаса с константами, но что поделать, не отправлять же запрос к ядру на каждый чих)

```python

class Geom2DType:
	ARC2 =  13027
	LINESEGMENT2 = 13025
	CONTOUR2 = 13072
	PLINE2 = 13085
	...

class Doc2:
	def selection2d_by_types(self, types: list[Geom2DType]):
		...
```


**Что исправлено:**
Геометрические типы это перечисление, поправил их отсутствие
Нельзя будет задать список произвольных целых чисел
