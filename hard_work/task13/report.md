## Задание

1. Изучите 22) "Важные принципы хорошего кода".

2. Найдите в своих (лучше) или чужих проектах три типичные для этих проектов управленческих шаблона (разных), и придумайте для каждого подходящую абстракцию, которая позволяет сделать то же самое существенно компактнее.

Опишите вкратце каждую абстракцию и дайте примеры кода "было-стало".

## Решение

1 -- легкий пример 2 -- обычный, 3 -- сложный
### Пример 1 (просто рефакторинг)
Рефакторим кривую работу с файлами

было
```python
try:
    f = open(DEFAULT_JOB_PROPS_FILENAME)
    default_job_props = json.load(f)
    
except:
    showerror(title="Ошибка", message="Некорректный или отсутствующий файл параметров УП")
finally:
	f.close()

try:
    f = open(DEFAULT_PATH_PROPS_FILENAME)
    default_path_props = json.load(f)
except:
    showerror(title="Ошибка", message="Некорректный или отсутствующий файл параметров траектории")    
finally:
	f.close()
```

стало чуть аккуратнее
```python
if not os.path.exists(DEFAULT_JOB_PROPS_FILENAME):
	showerror(title="Ошибка", message="Некорректный или отсутствующий файл параметров УП")
	exit()

if not os.path.exists(DEFAULT_PATH_PROPS_FILENAME):
	showerror(title="Ошибка", message="Некорректный или отсутствующий файл параметров траектории")
	exit()
	
with open(DEFAULT_JOB_PROPS_FILENAME) as f:
		default_job_props = json.load(f)

with open(DEFAULT_PATH_PROPS_FILENAME) as f:
		default_path_props = json.load(f)

```


## Пример 2 -- `cond` из лиспа на питоне
удобный множественный выбор без цепочек `if ... elif ... else ...`

**Реализация**
```python
ConditionValue = tuple[bool, Any]

def cond(condition_values: list[ConditionValue], default_value: Any) -> Any:
    for condition, value in condition_values:
        if condition:
            return value
    return default_value
```

**Пример использования**
Было
```python
	Ne = ...
    degrees = ...
    Nv = ...
    if Nv == 0:
	    return CCTopo.EMPTY
	if Nv == 1:
		return CCTopo.POINT
	if (Nv == 2) and (Ne == 1):
		return CCTopo.SEGMENT
	if all([degree == 2 for degree in degrees]):
		return CCTopo.CONTOUR
	if Ne == Nv - 1:
		return CCTopo.PLINE
    
    return CCTopo.UNKNOWN
```
Стало
```python
    Ne = ...
    degrees = ...
    Nv = ...
    condition_values = [(Nv == 0, CCTopo.EMPTY),
                  (Nv == 1, CCTopo.POINT), 
                  ((Nv == 2) and (Ne == 1), CCTopo.SEGMENT),
                  (all([degree == 2 for degree in degrees]), CCTopo.CONTOUR),
                  (Nv == Ne - 1, CCTopo.PLINE)
                  ]
    return cond(condition_values, CCTopo.UNKNOWN)
```

Стало короче, условия идут единым блоком, можно отделить логику принятия решения от исполнения.

## Пример 3. Проверка предусловий
Моя идея, мое исполнение.
Декоратор для проверки предусловий (проверяет условие, если неверно -- ставит статус = `ERR`  и возвращает `None`, также можно сохранять последнее пользовательское сообщение об ошибке).
Реализация внутри построена на `try-except`, но это надежно инкапсулировано в одном методе одного класса и не выходит за его пределы.

Это топорное решение, зато быстро позволяет рефакторить ошибочные состояния.

**Реализация**
```python
# *** precondition.py ***
from enum import Enum

DEFAULT_ERROR_MESSAGE = "Unknown check error"

class Status(Enum):
    NIL = 0
    OK = 1
    ERR = 2
    
class CheckError(Exception):
    def __init__(self, message: str = ""):
        self._message = message
    
    def __str__(self):
        return self._message
        
class Precondition:
    def __init__(self):
        self._status = Status.NIL
        self._error_text = "NIL"
        
    def pre_check(condition: bool, message: str = DEFAULT_ERROR_MESSAGE):
        if not condition:
            raise CheckError("!SoftAssertionError: " + message)
    
    @property
    def error_message(self):
        return self._error_text
    
    @property
    def status(self):
        return self._status
        
    def on(func):
        def inner(self, *args, **kwargs): 
            try:
                ans = func(self, *args, **kwargs)
                self._error_text = "OK"
                self._status = Status.OK
            except CheckError as err:
                self._error_text = str(err) 
                self._status = Status.ERR
                ans = None
            return ans
        return inner
    
    @property
    def is_OK(self) -> bool:
        return self.status == Status.OK
```

**Пример использования**
Было
```python
def remove_vertex(self, vert_id: int):
    if not self.has_vert_id(vert_id):
        self._c_status == Status.ERR
        return
        
    for edge in filter(lambda ed: ed[0] == vert_id or ed[1] == vert_id, self.edges_values):
        ...
```

Стало
```python
@Precondition.on
def remove_vertex(self, vert_id: int):
	self.pre_check(self.has_vert_id(vert_id))
    
    for edge in filter(lambda ed: ed[0] == vert_id or ed[1] == vert_id, self.edges_values):
	    ...
```
(+) сокращение кода в 3 раза, 
(+) синтаксически сильно удобнее: нет условия, есть явное указание на предусловие не только в комментарии
(-) возможно возрастут временные затраты 
(-) если забыть декоратор, работать будет, но криво -- при проверке предусловия будет выброшено настоящее исключение
## Дальнейшие планы
- добавить логирование в обработку предусловий
- добавить логирование как декоратор
- возможно добавить обработку предусловий
- поискать математическое определение факторизации
- добавить несколько условий и сообщений, аналогично `cond`
## Выводы
- Факторизация это обобщение принципа `DRY`
- В `Python` для факторизации можно использовать декораторы


