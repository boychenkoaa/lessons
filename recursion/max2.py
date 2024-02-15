def bubble(elem, max2, max1):
    if elem > max2:
        elem, max2 = max2, elem
    if elem > max1:
        elem, max1 = max1, elem
    return max2, max1

def max12_base(li: list, left_index: int, max2: float, max1: float):
    if left_index == len(li) - 1:
        return bubble(li[-1], max2, max1)[1]
    else:
        max2, max1 = bubble(li[left_index], max2, max1)
        return max12_base(li, left_index+1, max2, max1)

def max2(li: list):
    if len(li) < 2:
        raise ValueError('List is too short')
    elif len(li) == 2:
        return min(li)
    else:
        max2, max1 = min(li[0], li[1]), max(li[0], li[1])
        return max12_base(li, 2, max2, max1)

	
