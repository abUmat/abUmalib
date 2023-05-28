# my module
from misc.typing_template import *
# my module
# # https://nyaannyaan.github.io/library/graph/cycle-detection.hpp
def cycle_detection(g: Graph, directed: bool=True) -> List[Tuple[int, int]]:
    pidx = [-1] * len(g)
    vis = [0] * len(g)
    cycle = []
    finish = 0
    def dfs(cur: int, pval: int, par: int) -> int:
        nonlocal finish
        pidx[cur] = pval
        vis[cur] = 1
        for dst in g[cur]:
            if finish: return -1
            if not directed and dst == par: continue
            if pidx[dst] == pidx[cur]:
                cycle.append((cur, dst))
                return dst
            if vis[dst]: continue
            nxt = dfs(dst, pval, cur)
            if nxt != -1:
                cycle.append((cur, dst))
                if cur == nxt:
                    finish = 1
                    return -1
                return nxt
        pidx[cur] = -1
        return -1
    for i in range(len(g)):
        if vis[i]: continue
        dfs(i, i, -1)
        if finish:
            cycle.reverse()
            return cycle
    return []