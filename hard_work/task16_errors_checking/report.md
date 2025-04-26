Общее описание:
1, 2 -- простые единичные проверки "на дурака". Кажутся немного надуманными, но может быть я неправ.
3 -- замена множественных проверок состояния на отлов выброшенного исключения при вызовах API (для запроса)
4 -- поднимаем валидацию данных формы ввода в Qt на новый уровень абстракции
5 -- разделяем логические слои и через это разносим запросы к предусловиям


## Пример 1 

Конвертация кватернионов в углы Эйлера

**Было**: кватернион может оказаться вырожден, у самого класса `Quaternion` соответствующих проверок нет.
```python
class AnglesConverter:
    ...
    def q2euler(self, q: Quaternion, euler_type: EulerType) -> vec3:
        if q.R <= self.epsilon:
            return None
```
 
 **Стало**
Улучшено: унаследовались и добавили предусловие. Теперь кватернион проверяет себя сам, а конвертер проверяет его состояние -- в ошибке или нет :) Можно сказать, что фактически проверка вынесена за пределы класса.

```python
class NonZeroQuaternion(Quaternion, Precondition)
    @Precondition.on
    def __init__(self, w: float,x: float, y: float, z: float):
        super().__init(w,x,y,z)
        self.pre_check(self.R <= self.epsilon):

class AnglesConverter(Precondition):
    ...
    def q2euler(self, q: NonZeroQuaternion, euler_type: EulerType) -> vec3:
        self.pre_check(q.is_OK)
        ...
   
```

## Пример 2 

**Было** -- функция нахождения угла по паре синус / косинус
```python
def angle_by_sincos(sin_value: float, cos_value: float) -> float:
    assert sign_eps(sin_value**2 + cos_value**2 - 1) == 0
    ans = acos(cos_value)
    if sin_value < 0:
        ans *= -1
    return ans
```

**Стало**: она в целом ,была кучерявая -- во первых, надо обобщить на произвольную точку, и исключить ее нулевое значение по аналогии с предыдущим примером. 

```python
class NonZeroPoint2(Point2, Preсondition):
    def __init__(self, x: float, y: float, epsilon = EPSILON):
        self.pre_check(x**2 + y**2 > epsilon**2)
        self._x, self._y = x, y

def angle_by_point(p: NonZeroPoint2) -> float:
    return math.atan2(p.y, p.x)
```

Cлучай `x=y=0`, соответственно можно обнаружить раньше.

## Пример 3

**Было**: много вызовов перестраховок -- проверок внутреннего состояния пространства модели.

```python
class Doc2D(Precondition)    
    @property
    def active_plane3d_offset(self):
        app = self._app
        idoc3d = self.parent_doc3d
        if idoc3d == None or \
        idoc3d.DocumentType != app.constants.ksDocumentPart:
            return None
        
        idoc3d1 = app.api7.IKompasDocument3D1(idoc3d)
        eo = idoc3d1.EditObject
        if eo==None or eo.FeatureType != app.constants_3d.o3d_entity:
            return None
            
        mo = app.api7.IModelObject(eo)
        if mo.ModelObjectType != app.constants_3d.o3d_sketch:
            return None
            
        sk = app.api7.ISketch(mo)
        plane = sk.Plane
        if plane.ModelObjectType != app.constants_3d.o3d_planeOffset:
            return None
        
        plane3d = app.api7.IPlane3DByOffset(plane)
        return plane3d.Offset
```

**Стало**: все проверки однотипные и преследуют одну цель -- избежать исключения `AttributeError`. (Классы API формируются динамически). Методы работают только на чтение, поэтому в данном случае считаю допустимым принудительно подавить   `AttributeError` и лишь в конце проверить, сработало исключение или нет.

```python
from contextlib import suppress

class Doc2D(Precondition)    
    @property
    def active_plane3d_offset(self):
        ans = None
        # 
        with contextlib.suppress(AttributeError):
            app = self._app
            idoc3d = self.parent_doc3d
            idoc3d1 = app.api7.IKompasDocument3D1(idoc3d)
            eo = idoc3d1.EditObject
            mo = app.api7.IModelObject(eo)
            sk = app.api7.ISketch(mo)
            plane = sk.Plane
            plane3d = app.api7.IPlane3DByOffset(plane)
            ans = plane3d.Offset
            
        self.pre_check(ans != None)
        return ans

```

Возможно, и эту схему стоит завернуть в декоратор. Отмечу, что если есть операции на запись -- нужно по честному переопределять контекстный менеджер.

## Пример 4

**Было**: валидация параметров алгоритма не отходя от кассы.
```python
try:
    angle = float(str_snake_angle_deg.get())
    step = float(str_snake_step.get())
    manipulator2d.insert_snake_of_dr_objects(...)
except:
    QErrorMessage().showMessage('Неверные числовые значения')

```

**Решение**:
самопальные валидаторы + свой класс формы ввода параметров, которому на вход скармливается валидатор для всего алгоритма
```python
class AlgoParameter(Generic[T]):
    def validate(self, value: T)
        ...

    @property
    def description(self) -> str:
        return self._description
    
    @property
    def name(self) -> str:
        return self._name


class AlgoSpecification(Generic[T], Precondition):
    ...
    # команда, ставит статус
    def validate(self, values_dict: dict)
        ...

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

class AlgoCommand(AlgoSpecification):
    def __init__(self, command_func: callable):
        self._commmand = func
        
    def do(self, params_dict: dict):
        self.validate(params_dict)
        self.pre_check(self.is_OK)
        self._command(**params_dict)
        
class AlgoParemeterFrame(QFrame):
    def __init__(parent, ok_command: AlgoCommand):
        super.__init__(parent)
        self._command = ok_command
        self._build()

    # тут размещение элементов ввода в соответствии со спекой на алгоритм и задание им валидаторов из спеки
    def _build(self):
        ...

    # дергаем параметры из полей ввода
    def self._get_params(self) -> dict:
        ...

    # меняет меточку
    def set_status(self):
        ...
    
    # обработчик нажатия OK
    def on_OK(self):
        d = self._get_params()
        self.pre_check(self.is_OK)
        self.do(d)
        self.set_status(self.message)
    
    
```
Соответственно, код самого окна для алгоритма змейки
```python
class SnakeCommand(AlgoCommand)
    # наследуемся и прописываем валидаторы
    ...

...

class MainWindow(QMainWindow):
    ...
    def on_snake(self):
        snake_command = SnakeCommand()
        self.showAlgoDialog(snake_command)
```

## Пример 5

**Задача**: выдернуть из Компаса выделенный элемент, найти все связанные с ним примитивы (`connected_chain`) и преобразовать их в собственный класс траекторию `SketchPath2d`.

**Было**. Смешивание логических слоев: чтения из пространства модели, конвертации, алгоритма над своими типами, записи -- отсюда проверки "в лоб".

```python
class doc2d:    
    def connected_chain(self, first_segment):
       nb = self.nb_of(first_segment)
        if len(nb) != 1:
            return [first_segment]
        ans = [first_segment, nb[0]]
        
        nb =  self.nb_of(ans[-1])
        while len(nb) == 2:
            new_elem = nb[0] if nb[1].Reference == ans[-2].Reference else nb[1]
            ans.append(new_elem)
            nb = self.nb_of(ans[-1])

    # тут проверки всех типов вразнобой
    def autoline_to_SketchPath2d(self, linesegment) -> SketchPath2d:
        chain = self.connected_chain(linesegment)
        if chain[0].Type != CURVETYPE_LINESEGMENT2:
            return None
        
        constraints = self.nb_constraints_of(chain[0])
        if len(constraints) >= 2:
            return None
        ...
        # пошел алгоритм, внутри него еще свои проверки
```

**Стало**:
Отдельные классы для чтения, для конвертации, для обработки.  Все условия "от дурака" разнесены по соответствующим классам в предусловия.

 Класс для чтения из пространства модели (тут обернуты ошибки неверного выделения или некорректной топологии) 
 ```python
# модельное пространство -> объекты API
class Doc2D(Precondition):
    def nb_of(self, drawing_object) -> set:
        ...
    
    #тут предусловие что выделен ровно один и условия учета топологии
    @Precondition.on
    def get_autoline(self):
        ans = self.selection([LINESEGMENT2, ARC2])
        self.pre_check(len(ans) == 1)
        prev = None
        nb = self.nb_of(current_seg)
        while len(nb) == 1:
            # на случай закольцовки
            if nb[0] == ans[0]:
                break
            ans.extend(nb)
            prev = nb[0]
            nb = self.nb_of(current_seg).discard(prev)
            
        self._get_autoline_status = GetAutolineStatus.OK
        self.warning_if(len(nb) > 1, "Fork")
        return ans
    
```

Конвертер (тут обернуты ошибки конвертации)
```python
# конвертер -- при чтении из модельного простратсва все ошибки остаются здесь. На выходе -- свои классы
class ksGeomConverter:
    def curve2geomprimitive(self, curve) -> GeomPrimitive:
        ...

# объекты API геометрические <-> геометрия
class ksGeomConveter:
    ...
    # вот тут выбор типа геометрии -- от него не уйти
    def curve2segments(self, curve2d):
        ...
        if curve2d.curve_type == LINESEGMENT2:
            ...        
        elif urve2d.curve_type == ARC2:
            ...
        else:
            ...
        
    
# объекты API рисуемые <-> траектории
class ksDrawingConverter(ksGeomConverter):
    ...

    def do2segment_props(do) -> PathProps:
        hyperlink_str = drawing_object.GetHyperLinkParam()[0]
        return SegmentProps().from_str(hyperlink_str)

    def do2path_props(do) -> PathProps:
        hyperlink_str = drawing_object.GetHyperLinkParam()[0]
        return PathProps().from_str(hyperlink_str)

    @Precondition.on
    def do2tp_segment_list(self, drawing_object) -> list[ToolPathSegment]:
        seg_props =    self.do2segment_props(do)    
        self.pre_check(seg_props.is_OK)
        curve2d = drawing_object.GetCurve2D()
        segments = self.curve2segments(curve2d)
        ans = [ToolPathSegment(seg, segment_props) for seg in segments]
        return ans
        
    @Precondition.on
    def autoline2tp(self, autoline) -> ToolPath:
        self.pre_check(len(autoline)>0)
        tp_props = self.do2path_props(autoline[0])
        self.pre_check(tp_props.is_OK)
        ans = ToolPath(tp_props)
        all_segments = sum(map (self.do2tp_segment_list,autoline), start = [])
        ans.extend(all_segments)
        self.pre_check(ans.is_OK)
        return ans
    
```

Пример использования короткий -- все скрыто под капотом
```python
autoline = doc2d.get_autoline()
tool_path = converter.autoline2tp(autoline)
```

## Общий вывод
Спасибо, арсенал полезных приемов рефакторинга пополнился, теперь знаю как увеличить надежность
