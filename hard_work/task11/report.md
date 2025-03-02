## Ясный код-2 

### 2. Уровень класса

**2.1 Нарушение SRP**
Класс работы с 2д-документом


<details>
<summary>Много кода</summary>

 ```
class KompasManipulator2D:
    def __init__(self, app: KompasApp):
        ...
    
    @property
    def api7(self):
        ...
    
    @property
    def active_doc2d(self):
        ...
    
    def update_parentdoc3d(self):
        ...
        
    def to5(self, object7):
        ...
    
    @property
    def active_plane_offset(self):
        ...
    
    def add_macroobject_to_parent3d(self, name):
        ...
    
    def linestyle(self, style_num: int):
        ...
        
    def insert_arrow_to_active_doc(self):
        ...
        
    @property
    def active_view(self):
        ...
        
    def layer(self, layer_num: int):
        ...
    
    def layer_comment(self, layer_num: int):
        ...
    
    @property
    def drawing_container(self):
        ...       
        
    def selection2d(self, types: list|None = None):
        ...

    def repair_slice_simple(self, epsilon = 0.1):
        ...  
    
    def insert_hyperlink(self, drawing_objects, text):
        ...
    
    def approximate_curve(self, curve, eps, max_rad) -> int:
        ...
    
    def add_point(self, xy: Point2, point_style: int = 0):
        ...
    
    def show_BE_of_contour(self, dr_contour):
        ...
        
    def delete_all_points(self):
        ...
            
    def update_BE_of_contours(self):
        ...
    
    def add_linesegment(self, begin, end):
        ...
    
    def add_arc(self, begin, mid, end):
        ...
        
    def add_LA(self, seg23: tuple[float]):
        ...
    
    def constraints_of(self, dr_object):
        ...
    
    def nb_constraints_of(self, dr_object):
        ...
    
    def nb_of(self, dr_object):
        ...
    
    def connected_chain(self, first_segment):
        ...
        
    def layer_str_of(self, dr_object):
        ...
    
    def hlink_str_of(self, dr_object):
        ...
        
    def reverse_linesegment(self, linesegment):
        ...
        
    def reverse_arc(self, arc):
        ...
            
    def ilinesegment_raw(self, linesegment):
        ...
    
    def iarc_raw(self, arc):
        ...
    
    def icontour_is_LA(self, icontour):
        ...
    
    def idrawing_object_to_raw(self, drawing_object):
        ...
    
    def icontourLA_raw(self, icontour):
        ...
    
    def reverse_drcontourLA(self, dr_contour):
        ...        
    
    #test
    def drawing_object_BE(self, drawing_object):
        ...
    
   ```
   
   ``` 
    def dr_contour_to_SketchPath2Dv2(self, dr_contour) -> SketchPath2d:
        ...  
    
    
    def autoline_to_SketchPath2d(self, linesegment) -> SketchPath2d:
        ...
    
    def add_autolineL(self, xy_list: list[tuple[float, float]]):
        ...
    
    def add_contour_from_xy_list(self, xy_list):
        ...
    
    def insert_snake_of_dr_objects(self, dr_objects: list, angle, step, start_dist = 0, sag = 1.0):
        ...
    
    def polygonize_dr_objects(self, dr_objects: list, close_all: bool = False, sag: float=0.01) -> MultiPolygon2:
        ...
    
    def LA_to_seg23(self, dr_object):
        ...
        
    def save_tmp_LA(self, tmp_obj):
        ...
    
    # если нельзя создать ограничение, вернет  False
    def add_2LA_merge_constraint(self, dr_object_first, dr_object_second):
        ...
    
    def dr_object_to_pline2(self, dr_object, sag) -> Pline2:
        ...
   
    # test!
    def pline2d_to_SketchPath2d(self, ipolyline2d) -> SketchPath2d:
        ...
        
    def dr_object_to_SketchPath2D(self, dr_object) -> SketchPath2d:
        ...
        
    def reverse_dr_object(self, dr_object):
        ...
        
    def reverse_selection(self):
        ...
        
    def dr_contourLA_to_autoline(self, dr_contour):
        ...
```
</details>

*Проблема*: много разноплановых методов. Очень тяжело вносить изменения. Неоднократно ловил себя на том, что добавляю одно и то же дважды.

*Решение*. Вынести команды и запросы в отдельные классы или даже функции. В самом классе оставить только самые базовые запросы, и само состояние.

**2.2 Cлишком маленький класс**

Класс из одного метода и одного состояния.
```
class iBlock():
    def __init__(self):
        pass
    
    def __str__(self):
        return "\n <<< ! abstract block ! >>> \n"
```
ну это интерфейс, но наследники тоже не сильно отличались, вот наследник

```
class kwARCOFblock(txtBlock):
    def __init__(self, txt: str):
        super().__init__("CALL arcof\n"+txt)
```

*Проблема*: перезаклад, переусложнение. На самом деле не критичное, но можно и более красиво сделать.

*Решение*: обойтись просто `NamedTuple`-ами и регулярками, сделать сразу класс для набора блоков, их немного, можно один метод для каждого типа.


**2.3 Чужой метод**

самый первый пример (SRP) тоже подходит под это описание, приведем еще один 

```
class ggConnectedTopology (Enum):
    UNKNOWN = -1
    EMPTY = 0
    POINT = 1
    SEGMENT = 2
    PLINE = 3
    CONTOUR = 4

class ConnectedGeomGraph:
	def __init__(self):
		self._gg = GeomGraph()
		
	@property
	def topology(self) -> ggConnectedTopology:
		Nverts = len(self._gg.all_vertices)
        degrees = [p23ext.ext for p23ext in self._gg.all_vertices]
        count2 = degrees.count(2)    
        count1 = degrees.count(1)
        if Nverts == 0:
            return ggConnectedTopology.EMPTY
        if Nverts == 1:
            return ggConnectedTopology.POINT
        if Nverts == 2:
            return ggConnectedTopology.SEGMENT
        if count2 == Nverts:
            return ggConnectedTopology.CONTOUR
        if count1 == 2 and count2 == Nverts - 2:
            return ggConnectedTopology.PLINE        
        return ggConnectedTopology.UNKNOWN
```

*Проблема*: метод `topology` просится не только для связного геом графа, но и для обычного -- в виде списка для компонент связности. А связный граф, получается, должен брать топологию у обычного... круг замкнулся.

*Решение*:  их обоих унаследовать от общего предка и переопределить по своему метод в каждом, пусть и с дублированием кода. Тем более что реализован `DFS` с параметром-функцией при обходе.

**2.4 Заполнение класса из нескольких мест**

Есть у меня класс `CUD`, который хранит информацию о том, что в итоге сделал алгоритм (какие сущности обновил, какие удалил и какие создал -- для компактного хранения истории, `undo`, `redo` и тому подобное)

```
@dataclass
class idGeom:
	id: int
	geom: iGeom

@dataclass
class CUD:
	id_geom_to_remove: set[idGeom]
	id_geom_to_update: set[idGeom]
	id_geom_to_update: set[idGeom]
```

В нынешнем варианте он наполняется сначала при парсинге запроса (заполняются айди), потом при выполнении команды (заполняются геометрии для добавления), потом при работе с хранилищем (полное заполнение). 

*Проблема*: сложно отслеживать эволюцию состояния.

*Решение*: сделать несколько иммутабельных классов - базовый - наследник - наследник. Это не частый запрос, можно позволить себе копировать предыдущее состояниее либо вообще создавать наследника.

**2.5 Зависимость класса от деталей реализации другого класса**

Есть у меня пока что "наиболее общая" змейка, которая умеет заполнять полигоны с отверстиями.

```
@dataclass
class CombSegmentIntersection:
    start_index: int
    pline: Pline2

@dataclass
class RasterPoint:
	...
	
class Comb:
	...

@dataclass
class Beads:
	...

class RasterLevels:
	...

# главная функция
def snakes_of_polygon(polygon: Polygon2, distances: list[float], angle: float) -> list[Pline2]:
```

Классы `RasterPoint` `Comb`, `Beads` и `RasterLevels` Их поля публичны, и они, если надо, знают все друг о друге, и могут друг друга менять.   

*Проблема*: сильная связанность четырех классов

*Решение*: не делать ничего. Этот случай мне видится исключением. Внешний мир интересует результат функции `snakes_of_polygon` Соответственно, если тесты функция проходит -- лучше потратить время на что-то другое.  
Фактически представляют внутренние для "змейки" структуры, и никак не взаимодействуют с внешним миром, только друг с другом.


**2.6 Приведение родителей к дочерним классам**

Тут будет хейт чужой работы.

Пример из моего использования API компаса-3д.
```

new_plane = self.aux_container.Planes3D.Add(self.const3d.o3d_planeOffset)
op = self.api7.IPlane3DByOffset(new_plane)
op.BasePlane, op.Direction, op.Offset, op.Name = base_plane, True, z_offset, plane_name


```

1. Первая строчка создает плоскость со смещением (аргумент -- тип плоскости), а возвращает указатель просто на плоскость (абстрактный класс). 
2. Вторая строчка делает преобразование обратно от абстрактного к дочернему, иначе его не задать. 
3. Третья строчка заполняет параметры плоскости

*Проблема*: экономия на спичках => неудобство работы с API, особенно при отсутствии хорошей документации. 

Преобразование типа задумано штатно -- видимо, чтобы не разводить кучу методов `AddPlaneByOffset`, `AddPlaneByAngle` ... Один метод возвращает один указатель -- красиво же!

Допустим, но для полного задания объекта, чтобы решатель не встал в ошибку (родительская плоскость, смещение, направление нормали, имя) -- нужно все равно делать приведение типа и заполнять соответствующие поля (!)

*Решение*: расплодить кучу методов, у них не более десятка видов задания плоскостей и вряд ли их будет 100. А даже если будет -- они все равно все разные! Чтобы каждый метод сразу возвращал нужный указатель. Список параметров тоже можно сделать аргументами либо отдельным классом. 

**2.7 Каскадное создание наследников**

Продолжаем историю с блоками
Основная их проблема -- даже не малый объем одного класса
Наконец-то я понял, что мне тут не нравится.

Есть четыре базовых класса
```

class pointBlock(iBlock):
    def __init__(self, pt_num: int, p9: P9):
        super().__init__()
        self.pt_num = pt_num
        self.p9 = p9
    
    def __str__(self):
        return "<<< " + str(self.pt_num) + " | " + str(self.p9) + ">>>"

class txtBlock(iBlock):
    def __init__(self, txt: str):
        super().__init__()
        self.txt = txt
    
    def __str__(self):
        return self.txt

class Job:
	def __init__(self, name):
        ...
        
    def append(self, new_frame: plineFrame):
        ...
    
    def pop(self, index):
        ...
        
    def swap(self, index1, index2):
        ...
    

class iPostprocessor:
	def make_nc(self, job: Job) -> str:
        ...

```

*Проблема*: 
Для добавления робота Кавасаки мне нужно создавать аж 4 новых класса, зависимых друг от друга: `kwPointBlock`, `kwTxtBlock`, `kwJob`, `kwPostprocessor`  -- раскиданные по разным модулям.
А для Яскавы нужно добавить, соответственно `yPointBlock`, `yTxtBlock`, `yJob`, `yPostprocessor`. А для G-кода -- `GCodePointBlock` ...

*Решение.* 
Расширить полномочия класса `PostProcessor`, добавив туда и изменение порядка блоков, и редактирование блоков, и собственно выдачу УП.
Все равно у каждого постпроцессора свой специфичный набор команд.

Это лишь часть глобальной проблемы, но для уже известных нам роботов она решаема. Про вновь добавляемых роботов будет пункт 3.1

**2.8 Переопределение родительских методов в наследниках**
```
class DiGraph(Generic[T]):
	#реализован через списки смежности
	...

	# запрос, предусловий нет
	# None если нет ребра
	def get_edge_value(self, edge_id: EdgeID) -> T:
		...

	def has_edge_id(self, edge_id: EdgeID) -> bool:
        ...

class BiGraph(DiGraph):
	# запрос, предусловий нет
	# None если нет ребра
    def get_edge_value(self, edge_id: EdgeID) -> T:
        return super().get_edge_value(tuple(sorted(edge_id)))
    
    # запрос, предусловий нет
    def has_edge_id(self, edge_id: EdgeID) -> bool:
        return super().has_edge_id(tuple(sorted(edge_id)))

```
*Проблема*: нарушение LSP
*Решение*: наследоваться от общего предка

### 3. Уровень приложения

**3.1 Каскадная модификация классов**

*Проблема*:  при добавлении нового робота (мы продаем Яскаву и Кавасаки -- а у заказчика Кука, ему нужно только ПО) вполне вероятно переписывание всей программы, потому что, например, заказчику нужна интерпретация сплайнами и он понимает как его робот это будет делать. Или какие-то более тонкие отличия Куки от Яскавы и Кавасаки, которые невозможно формализовать в ТЗ на предварительном этапе переговоров с заказчиком.

*Решение:* платить будет заказчик. Вообще, нужно составлять подробную спецификацию отличий одного от другого, и принимать решение на основе этого, что сносим, что оставляем.

Для  подобной работы требуется специалист по этим роботам (у них тоже не все возможности документированы), делать "универсальную" модель робота можно, имея на руках подробные спецификации и опыт по всем основным производителям. Это очень затратно по времени. Если повезет, то можно обойтись минимальными изменениями. Если не повезет -- придется переписывать половину ПО. И платить за это будет... заказчик.

**3.2 Переусложненные паттерны**

Когда-то я выучил паттерн "медиатор" и решил, что ничего другого не нужно :)

Дан самый простой класс точек. 

А вдруг мне понадобится генерить айдишники, как в кривой мортона? чтобы по айдишнику сразу можно было оценить расстояние между точками? Добавляем! Сделал генератор "айдишников". А еще кд-дерево к нему прикрутил из коробки. На случай частых запросов на ближайший. Ну и само хранилище точек, конечно же не в виде словаря, а красно-черного дерева! 

А еще добавил медиатор чтобы все эти штуки между собой общались.

```
class SmartPoints:	 
  def __init__(self):
	  self._mid_container = mIDContainer()
	  self._mid_generator = midGenerator()
	  self._mkd_tree = mkdTree()
	  self._points_mediator = PointsMediator(self._mid_container, self_.mid_generator, self._mkd_tree)
	  self._mid_container.set_mediator(self._points_mediator)
	  self._mid_generator.set_mediator(self._points_mediator)
	  self._mkd_tree.set_mediator(self._points_mediator)

```

_Проблема_: перезаклад и переусложнение по неопытности. Погреб для картошки превратился в бомбоубежище (криво спроектированное).

_Решение_:  айди-генератор и кд-дерево давно выпилены, а SmartPoints представляют собой один класс. Иначе это будет слишком мелкое дробление. Если понадобятся постоянные запросы к кд-дереву, можно сделать еще одни точки с использованием именно кд-дерева. Интерфейс Points для этого имеется.
