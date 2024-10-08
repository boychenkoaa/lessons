# Урок 1. Цикломатическая сложность

---
## Пример 1
Вводные
- Я не оптимизирую "вычислительную" часть
- лечим метод point_check

Рефакторинг
1.  Первые два параметра используются только вместе -- заменяем на один
2.  flag увеличивается на 1 вместе с добавлением элементов в массивы. Во первых это не флаг тогда, а во вторых всегда флаг=сумме длин массивов -- дублирование состояния без особых на то причин. Убираем эту переменную
3. переименовал функцию и некоторые переменные на более наглядные имена

Снижаем ЦС - в разделе <<стало>>:



### Было-1

```
def point_check(point_ind, s_l_of_edges, i_p_del, r_p_del, l_p_del):
    # проверка точки на совпадение с той, которую хотим удалить, проверяем не координату, а содержимое
    flag = - 1
    i_p_need_delete = []
    r_p_need_to_be_deleted = []
    l_p_need_to_be_deleted = []

    while i_p_del:
        test_edges = s_l_of_edges[point_ind].i_p
        if test_edges:
            for ed in test_edges:
                # если концы отрезков совпадают
                if ed.end == i_p_del[0].end:
                    flag += 1
                    i_p_need_to_be_deleted.append(ed)
                    break
            # pop тут, тк мб вариант (i_p_del и test_edges) != 0 и не имеют пересечений
            i_p_del.pop(0)
        else:
            break
            # сразу удалить этот отрезок ed из LRI_sorted_list[element].i_p

    # хотим проверить r_p, их вторая координата всегда равна нашей точке, поэтому
    # проверяем принадлежность точки отрезку

    while r_p_del:
        test_edges = s_l_of_edges[point_ind].r_p
        if test_edges:
            for ed in test_edges:
                test_class = ed.find_relative_position(r_p_del[0].beg, epsilon=0)
                if test_class in (PointLoc.ORIGIN, PointLoc.BETWEEN):
                    flag += 1
                    r_p_need_to_be_deleted.append(ed)
                    break
            r_p_del.pop(0)
        else:
            break

    while l_p_del:
        test_edges = s_l_of_edges[point_ind].l_p
        if test_edges:
            for ed in test_edges:
                test_class = ed.find_relative_position(l_p_del[1].beg)
                if test_class in (PointLoc.BETWEEN, PointLoc.DESTINATION):
                    flag += 1
                    l_p_need_to_be_deleted.append(ed)
                    break
            l_p_del.pop(0)
        else:
            break
    if flag == 1:  # если совпали оба пересекающихся в данной точке отрезка
        for el in i_p_need_to_be_deleted:
            s_l_of_edges[point_ind].i_p.remove(el)
        for el in r_p_need_to_be_deleted:
            s_l_of_edges[point_ind].r_p.remove(el)
        for el in l_p_need_to_be_deleted:
            s_l_of_edges[point_ind].l_p.remove(el)

        return point_ind
    return -1

```

### Стало-1

1. Три повторения одного и того же цикла по одному шаблону выделил в отдельную функцию `find_used_edges`
2. в этой функции используются ФП-фишки
3. внутри `while` `if` не нужен -- это проход по всем и последующая очистка
4. внутри for он не нужен тоже, можно сделать `filter`

```
def find_used_edges(edges_list, candidates_edges_list, condition_func) -> list:
    return list(filter( lambda candidate: any(condition_func(candidate, edge) in edges_list), candidates_edges_list))

# это, как по мне, вполне рабочее решение
def check_lri_record(lri_record: LRI, i_p_del, r_p_del, l_p_del):
    used_i_p = find_used_edges(lri_record.i_p, i_p_del, lambda e1, e2: e1.end == e2.end)
    used_r_p = find_used_edges(lri_record.r_p, r_p_del, lambda e1, e2: e2.find_relative_position(e1.beg, epsilon=0) in (PointLoc.ORIGIN, PointLoc.BETWEEN))
    used_l_p = find_used_edges(lri_record.l_p, l_p_del, lambda e1, e2: e2.find_relative_position(e1.beg, epsilon=0) in (PointLoc.BETWEEN, PointLoc.DESTINATION))
    l_p_del.clear()
    i_p_del.clear()
    r_p_del.clear()
    if len(used_i_p) + len (used_l_p) + len(used_r_p) == 2:
        lri_record.i_p = SortedKeyList(filter(lambda x: x not in used_i_p, lri_record.i_p)) 
        lri_record.r_p = SortedKeyList(filter(lambda x: x not in used_r_p, lri_record.r_p))
        lri_record.l_p = SortedKeyList(filter(lambda x: x not in used_l_p, lri_record.l_p))
        return True
    return False
```


## Пример 2

- Status.update_y - наш сегодняшний пациент
- он избыточно сложен
- метода лечения два -- упрощение условий и использование полиморфизма
- подробнее в разделе "стало"

### Было-2
```
class Edge:
    ...
    def get_y_coordinate_by(self, x):
        if abs(self.beg_x - self.end_x) < eps:
            return self.beg_y
        return self.beg_y + (self.end_y - self.beg_y) * (x - self.beg_x) / (self.end_x - self.beg_x)

class Status:
    ...
    
    def update_y(self, new_edge: Edge):
        """ 
        Returns a new edge sequence including the new_edge.
        The order of the edges corresponds to the order of the Status.
        """
        edges = self.new_list
        new_x, new_y = new_edge.beg_x, new_edge.beg_y

        if len(edges) == 1:  # если в списке только одно ребро, добавляем второе
            edge = edges[0]
            curr_y = edge.get_y_coordinate_by(new_x)
            if new_y == curr_y:  # если начала по y совпадают, добавить eps - ?
                return edge.get_sorted_list_for_status(new_edge)
            return [edge, new_edge] if new_y > curr_y else [new_edge, edge]

        # бинпоиск по позиции отрезка в статусе, искомая позиция находится между существующими
        modified_edges = [((-sys.maxsize, -sys.maxsize), (sys.maxsize, -sys.maxsize))]
        modified_edges.extend(edges)
        modified_edges.append(((-sys.maxsize, sys.maxsize), (sys.maxsize, sys.maxsize)))
        low = 0
        high = len(modified_edges) - 1
        while low <= high:
            mid = low + (high - low) // 2
            guess = modified_edges[mid]
            guess_y = guess.get_y_coordinate_by(new_x)

            if abs(guess_y - new_y) < eps:
                if guess.get_sorted_list_for_status(new_edge)[0] == guess:
                    low = mid
                else:
                    high = mid
                # сортируем отрезки по углу наклона, проверить внимательно на тестовых данных!
                # возможно удалить эту часть
                if guess.end_x <= new_edge.end_x:  # ищем минимальную x координату концов рёбер
                    if guess.end_y > new_edge.get_y_coordinate_by(guess.end_x):
                        high = mid
                        # сравниваем значение y в этой точке
                    else:
                        low = mid
                else:
                    if new_edge.end_y > guess.get_y_coordinate_by(new_edge.end_x):  # сравниваем значение y в этой точке
                        low = mid
                    else:
                        high = mid
            elif guess_y < new_y:
                low = mid
            else:
                high = mid

            if high - low == 1:
                break
        y_pos = low
        edges.insert(y_pos, new_edge)
        return edges
 ```       

### Стало -2
1. Классы `Edge` можно сравнивать двумя способами. Первый способ стандарнтый - как пару кортежей `(x1,y1),(x2,y2)`Второй способ -- "сравнение в статусе", более специфичен для реализуемого алгоритма (находится внутри старого while)
2. Чтобы бинарный поиск (точнее -- бисекция!) работала корректно, я просто сделаю наследника от `Edge` -- `StatusEdge` с переопределенным методом `__le__` и декоратором `@total_ordering`
3. Если вдруг припечет, то для `StatusEdge` можно явно вызвать и стандартное сравнение, удобно
4. Cравнение в статусе я не удержался и тоже переписал не просто избавлением от `else`, но и упрощением самих вычислений. В этом задании такое не приветствуется (нужно менять форму не меняя содержания), но когда я могу заменить пять сложных условий на два простых, мне сложно пройти мимо.

```
from functools import total_ordering

@total_ordering 
class Edge:
    ...
    # переименованный get_y_coordinate_by
    def x_to_y(self, x):
        if abs(self.beg_x - self.end_x) < eps:
            return self.beg_y
        return self.beg_y + (self.end_y - self.beg_y) * (x - self.beg_x) / (self.end_x - self.beg_x)
    
    def __le__(self, other):
        return self.beg, self.end < other.beg, other.end
        
    # добавили
    @property
    def slope(self):
        if self.is_vertical:
            return np.inf if self.end_y > self.beg_y else np.-inf
        return (self.end_y - self.beg_y) / (self.end_x - self.beg_x)

# сделал отдельный наследник для сравнения в статусе
@total_ordering     
class StatusEdge(Edge):
    def __lt__(self, other):
        x = self.beg_x
        y = self.beg_y
        other_y = other.x_to_y(x)
        return y + EPSILON < other_y or  abs(y - other_y) < EPSILON and self.slope < other.slope


# честно украденный стандартный bisect
# возвращает место в отсортированном массиве, куда вставлять новый элемент
# тут многовато условий, но это очень известная функция, ей простительно :)
def bisect_left(arr, val):
    if len(arr) == 0:
        return 0
    if val < arr[0]:
        return 0
    if arr[-1] < val:
        return len(arr)

    lo, hi = 0, len(arr) - 1

    while lo < hi:
        if val == arr[lo]:
            return lo
        elif val == arr[hi]:
            return hi

        mid = (lo + hi) // 2

        if val == arr[mid]:
            return mid
        elif val < arr[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo
 
# теперь сложность = 1
class Status:
    ....
    def update(self, new_status_edge: StatusEdge):
        new_pos = bisect_left(self.status_list, new_status_edge)
        self.status_list.insert(new_pos, new_status_edge)

```


---
## пример 3
- а вот это уже мой код
- препарируем метод `nearest_geom_connection`
- табличный метод позволил избавиться сразу от всего


### было - 3
```
# вспомогательные классы
class AnyHeadTail(Enum):
    ANY = "ANY"
    HEAD = "HEAD"
    TAIL = "TAIL"

@dataclass
class ConnectionParams:
    connection_point_type: AnyHeadTail
    repair_type: RepairType
    try_reverse: bool = True

@dataclass
class GeomConnection:
    to_head: bool = False
    is_reversed: bool = True
    distance: float = EPSILON

# препарируем метод nearest_geom_connection
class GeomContour:
    ...
    def nearest_geom_connection(self, new_primitive: GeomPrimitive, connection_params: ConnectionParams) -> GeomConnection:
        d = distance_pp
        H, T = self.BE
        B, E = new_primitive.BE
        BH, EH, BT, ET = d(B, H), d(E, H), d(B, T), d(E, T)
        
        ans = None
        connection_type, try_reverse = add_info.connection_point_type, 
        if connection_type == AnyHeadTail.HEAD:
            ans = GeomConnection(is_head = True, is_reversed = False, distance = EH)
            if try_reverse and BH < EH:
                ans.is_reversed = True
                ans.distance = BH
        
        elif connection_type == AnyHeadTail.TAIL:
            ans = GeomConnection(is_head = False, is_reversed = False, distance = BT)
            if try_reverse and ET < BT:
                ans.is_reversed = True
                ans.distance = ET
        
        elif connection_type == AnyHeadTail.ANY:
            ans = GeomConnection(is_head = True, is_reversed = False, distance = EH)
            if BT < EH:
                ans.to_head = False
                ans.distance = BT
            
            if try_reverse:
                if BH < ans.distance:
                    ans.to_head = True
                    ans.is_reversed = True
                    ans.distance = BH
                if ET < ans.distance:
                    ans.to_head = False
                    ans.is_reversed = True
                    ans.distance = ET
        return ans
```


### стало - 3

- табличная логика - простое перечисление вариантов в таблице -- помогла снизить ЦС до 1
- можно было бы сделать перечисление через декартово произведение, но мне это видится уже выхолащиванием...
еще можно было бы вытащить эту таблицу наружу -- но тогда пришлось бы внутри метода городить еще один словарь типа {"EH": EH, "ET": ET} что мне в данном примере тоже видится выхолащиванием, да и снаружи эта таблица как таковая пока не особо нужна
- но, справедливости ради, тестировать все равно нужно все случаи в таблице

```
class GeomContour:
    ...
    
    def nearest_geom_connection(self, new_primitive: GeomPrimitive, connection_params: ConnectionParams) -> GeomConnection:
        
        H, T = self.BE
        B, E = new_primitive.BE
        BH, EH, BT, ET = map(distance_pp, (B, E, B, E), (H, H, T, T))
        GC = GeomConnection
        geom_connection_table = \
        {("HEAD", False): (GC(True, False, EH)), \
        ("HEAD", True): (GC(True, False, EH), GC(True, True, BH)), \
        ("TAIL", False): (GC(False, False, BT)), \
        ("TAIL", True): (GC(False, False, BT), GC(False, True, ET)), \ 
        ("ANY", False): (GC(True, False, EH), GC(False, False, BT)),  \
        ("ANY", True): (GC(True, False, EH), GC(True, True, BH), GC(False, False, BT), GC(False, True, ET))
        }
        connection_type, try_reverse = connection_params.connection_point_type, connection_params.try_reverse
        return GeomConnection(min(geom_connection_table[(connection_type, try_reverse)], key = lambda gc: gc.distance)
```

стало покороче и поменьше условий


## Выводы 

1. До НГ ставлю себе задачу ввести метрику измерение ЦС вновь добавляемого кода.
2. При код-ревью обязательно буду автоматически измерять ЦС (настрою CI/CD), если превышает 10-15 -- это будет повод поговорить.
3. ЦС можно уменьшить, не вникая в сами вычисления (преобразования), а только лишь отслеживая логику исполнения, хотя удобнее конечно по возможности видеть картину целиком.

