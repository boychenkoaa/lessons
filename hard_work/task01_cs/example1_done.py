def find_used_edges(edges_list, candidates_edges_list, condition_func) -> list:
    return list(filter( lambda candidate: any(condition_func(candidate, edge) in edges_list), candidates_edges_list))

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