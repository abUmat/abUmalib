# my module
from misc.typing_template import *
# my module
def manacher(S: str) -> List[int]:
    '各iに対し, S[i-k+1:i+k-1]が回文となる最大のkを求める'
    c = 0
    n = len(S)
    res = [0] * n
    for i in range(n):
        l = c + c - i
        if i + res[l] < c + res[c]:
            res[i] = res[l]
        else:
            j = c + res[c] - i
            while i - j >= 0 and i + j < n and S[i - j] == S[i + j]: j += 1
            res[i] = j
            c = i
    return res

def manacher_even(S: str) -> List[int]:
    T = S.replace('', '$')
    res = manacher(T)
    return [x-1 for x in res][1:-1]
