from functools import reduce


def max2(li: list[int]) -> int:
    if len(li) < 2:
        raise ValueError("array is too short")
    a, b = li[0], li[1]
    if b < a:
        a, b = b, a
    return reduce(lambda ab, c: ab \
        if c <= ab[0] else \
        (c, ab[1]) if c <= ab[1] \
        else (ab[1], c), li[2:], (a, b))[0]

if __name__ == "__main__":
    print(max2([1,2,3,4,5])) # 4
    print(max2([5,4,3,2,1])) # 4
    print(max2([1,1,1,1,1])) # 1
    print(max2([0,0,1,0,1])) # 1 - для повторов
    print(max2([0,0,1,0,0])) # 0
