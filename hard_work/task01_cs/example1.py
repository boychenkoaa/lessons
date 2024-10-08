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