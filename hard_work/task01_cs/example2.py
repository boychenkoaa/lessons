# лечим Status.update_y

class Edge:
    ...
    def get_y_coordinate_by(self, x):
        if abs(self.beg_x - self.end_x) < eps:
            return self.beg_y
        return self.beg_y + (self.end_y - self.beg_y) * (x - self.beg_x) / (self.end_x - self.beg_x)
    def get_sorted_list_for_status(self, other):
        if self.end_x <= other.end_x:   # возможно просто <
            return [other, self] if self.end_y > other.get_y_coordinate_by(self.end_x) else [self, other]
        else:
            return [self, other] if other.end_y > self.get_y_coordinate_by(other.end_x) else [other, self]

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