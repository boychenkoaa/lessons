def bstH(array_size):    
    ans = -1
    while array_size > 0:
        array_size //= 2
        ans += 1
    return ans

def GenerateBBSTArray(a):
    a.sort()
    len_a = len(a)
    H = bstH(len_a)
    bst = [None] * len_a
    
    index_bst = 0
    for h in range(H,-1,-1):
        left = 2**h - 1
        step = 2**(h+1)
        for index_a in range(left, len_a, step):
            bst[index_bst] = a[index_a]
            index_bst += 1
    
    return bst
