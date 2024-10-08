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
        
    #  наклон прямой
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