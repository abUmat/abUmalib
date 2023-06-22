# https://judge.yosupo.jp/problem/vertex_add_subtree_sum
# my module
from misc.fastio import *
from segment_tree.segment_tree import *
from tree.heavy_light_decomposition import *
# my module
N, Q = rd(), rd()
A = rdl(N)
G = [[] for _ in range(N)]
for i in range(N - 1):
    G[rd()].append(i + 1)
hld = HeavyLightDecomposition(G)
seg = SegmentTree(N, 0, lambda x, y: x + y)
for i in range(N): seg.set(hld.down[i], A[i])
seg.build()
for _ in range(Q):
    cmd = rd()
    if cmd:
        u = rd()
        ans = 0
        def func(u: int, v: int) -> None:
            global ans
            ans += seg.prod(u, v)
        hld.subtree_query(u, 1, func)
        wtn(ans)
    else:
        p, x = rd(), rd()
        seg.add(hld.down[p], x)