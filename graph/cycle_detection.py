# my module
from misc.typing_template import *
# my module
# # https://nyaannyaan.github.io/library/graph/cycle-detection.hpp
def cycle_detection(g: Graph, directed: bool=True) -> List[Pair]:
    import sys
    sys.setrecursionlimit(10**8)
    n = len(g)
    for u, gu in enumerate(g):
        s = set()
        for v in gu:
            if u == v: return [(u, u)] # self-loop
            if not directed and v in s: return [(u, v), (v, u)] # multiple-edge
            s.add(v)
    pidx = [-1] * n
    visited = bytearray(n)
    cycle = []
    finish = 0
    def dfs(cur: int, par: int) -> int:
        nonlocal finish
        pidx[cur] = pval
        visited[cur] = 1
        for dst in g[cur]:
            if finish: return -1
            if not directed and dst == par: continue
            if pidx[dst] == pidx[cur]:
                cycle.append((cur, dst))
                return dst
            if visited[dst]: continue
            nxt = dfs(dst, cur)
            if nxt != -1:
                cycle.append((cur, dst))
                if cur == nxt:
                    finish = 1
                    return -1
                return nxt
        pidx[cur] = -1
        return -1

    for i, flg in enumerate(visited):
        if flg: continue
        pval = i
        dfs(i, -1)
        if finish:
            cycle.reverse()
            return cycle
    return []
