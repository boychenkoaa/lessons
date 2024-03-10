def bstH(array_size):    
    ans = -1
    while array_size > 0:
        array_size //= 2
        ans += 1
    return ans

def generatebbstarray(a: list):
    a_sorted = sorted(a)
    len_a = len(a_sorted)
    H = bstH(len_a)
    bst = [None] * len_a
    
    index_bst = 0
    for h in range(H,-1,-1):
        for index_a in range(2**h-1, len_a, 2**(h+1)):
            bst[index_bst] = a_sorted[index_a]
            index_bst += 1
    
    return bst