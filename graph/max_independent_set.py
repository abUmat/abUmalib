# my module
from gcc_builtins import *
from misc.typing_template import *
# my module
# https://nyaannyaan.github.io/library/graph/max-independent-set.hpp
def max_independent_set(g: Graph) -> List[int]:
    N = len(g)
    bs = [0] * N
    for i in range(N):
        for j in g[i]:
            bs[i] |= 1 << j
            bs[j] |= 1 << i
    res = 0
    q = [[0, 0, 0]]
    while q:
        i, cur, ignore = q.pop()
        if i == N:
            if popcountll(cur) > popcountll(res): res = cur
            continue
        bit = bs[i]
        if bit & cur or popcountll(bit & ~ignore) >= 2:
            q.append([i + 1, cur, ignore | 1 << i])
        if not bit & cur:
            q.append([i + 1, cur | 1 << i, ignore])
    return [i for i in range(N) if res >> i & 1]
