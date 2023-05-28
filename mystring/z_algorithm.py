# my module
from misc.typing_template import *
# my module
def z_algo(s: str) -> List[int]:
    n = len(s)
    res = [0] * n
    res[0] = n
    i, j = 1, 0
    while i < n:
        while i + j < n and s[j] == s[i + j]: j += 1
        res[i] = j
        if j == 0: i += 1; continue
        k = 1
        while i + k < n and k + res[k] < j:
            res[i + k] = res[k]
            k += 1
        i += k; j -= k
    return res
