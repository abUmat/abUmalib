# my module
from misc.typing_template import *
# my module
# https://judge.yosupo.jp/submission/107621
def enumerate_triangles(n: int, edges: List[int], f: Callable[[int, int, int], None]) -> None:
    '''
    n: Number of nodes
    edges: [frm << 20 | to]
    f: func(i, j, k) i, j, k is triangle
    '''
    g: Graph = [[] for _ in range(n)]
    deg = [0] * n
    for uv in edges:
        u, v = uv >> 20, uv & 0xfffff
        deg[u] += 1; deg[v] += 1
    for i, uv in enumerate(edges):
        u, v = uv >> 20, uv & 0xfffff
        if deg[u] > deg[v] or (deg[u] == deg[v] and u > v):
            edges[i] = v << 20 | u
    for uv in edges: g[uv >> 20].append(uv & 0xfffff)
    deg = [n] * n
    for i in range(n):
        for j in g[i]:
            deg[j] = i
        for j in g[i]:
            for k in g[j]:
                if deg[k] == i:
                    f(i, j, k)
