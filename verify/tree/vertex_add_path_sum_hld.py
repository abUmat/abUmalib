# https://judge.yosupo.jp/problem/vertex_add_path_sum
# my module
from misc.fastio import *
from segment_tree.segment_tree import *
from tree.heavy_light_decomposition import *
# my module
N, Q = rd(), rd()
A = rdl(N)
G = [[] for _ in range(N)]
for _ in range(N - 1):
    u, v = rd(), rd()
    G[u].append(v)
    G[v].append(u)

hld = HeavyLightDecomposition(G)
seg = SegmentTree(N, 0, lambda x, y: x + y)
for i in range(N): seg.set(hld.down[i], A[i])
seg.build()

for _ in range(Q):
    cmd = rd()
    if cmd:
        u, v = rd(), rd()
        ans = 0
        def func(u: int, v: int) -> None:
            global ans
            ans += seg.prod(u, v)
        hld.path_query(u, v, 1, func)
        wtn(ans)
    else:
        p, x = rd(), rd()
        seg.add(hld.down[p], x)