# my module
from misc.typing_template import *
# my module
# https://judge.yosupo.jp/submission/100889
# https://www.slideshare.net/wata_orz/ss-12131479 p.15
def enumerate_cliques(n: int, edges: List[int], f: Callable[[List[int]], None]) -> None:
    '''
    n: Number of nodes
    edges: [frm << 20 | to]
    f: func(a: list of nodes)
    '''
    g: Graph = [[0] * n for _ in range(n)]
    M = 0
    for uv in edges:
        u, v = uv >> 20, uv & 0xfffff
        assert(0 <= u and u < n and 0 <= v and v < n and u != v)
        assert(not g[u][v])
        g[u][v] = g[v][u] = 1
        M += 1
    assert(M <= 1 << 11)
    m = 2
    while m * m >> 1 < M: m += 2
    res = [0] * n
    def run(tg: List[int], p: int) -> None:
        n = len(tg)
        E = [0] * 64
        for i, u in enumerate(tg):
            for j, v in enumerate(tg):
                if g[u][v]:
                    E[i] |= 1 << j
        for i in range(n):
            E[i] |= 1 << i
        b = 0
        while 1:
            ok = 1
            for i in range(n):
                if b >> i & 1 and E[i] & b != b:
                    ok = 0
                    break
            if ok:
                pi = p
                for i, u in enumerate(tg):
                    if b >> i & 1:
                        res[pi] = u
                        pi += 1
                if pi:
                    f(res)
            if b == (1 << n) - 1:
                break
            b += 1

    large: List[int] = []
    visited = bytearray(n)
    for i in range(n):
        d = sum(g[i])
        if d > m:
            large.append(i)
            continue
        visited[i] = 1
        tg = [j for j in range(n) if g[i][j] and not visited[j]]
        res[0] = i
        run(tg, 1)
    run(large, 0)
