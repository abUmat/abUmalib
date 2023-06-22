# https://judge.yosupo.jp/problem/vertex_set_path_composite
# my module
from misc.fastio import *
from segment_tree.segment_tree import *
from tree.heavy_light_decomposition import *
# my module
mod = 998244353
N, Q = rd(), rd()
AB = [rd() << 30 | rd() for _ in range(N)]
G = [[] for _ in range(N)]
for _ in range(N - 1):
    u, v = rd(), rd()
    G[u].append(v)
    G[v].append(u)
hld = HeavyLightDecomposition(G)
def op1(x: int, y: int) -> int:
    a, b = x >> 30, x & 0x3fffffff
    c, d = y >> 30, y & 0x3fffffff
    e, f = c * a % mod, (c * b + d) % mod
    return e << 30 | f
def op2(x: int, y: int) -> int:
    a, b = x >> 30, x & 0x3fffffff
    c, d = y >> 30, y & 0x3fffffff
    e, f = a * c % mod, (a * d + b) % mod
    return e << 30 | f
seg1 = SegmentTree(N, 1 << 30, op1)
seg2 = SegmentTree(N, 1 << 30, op2)
for i, ab in enumerate(AB):
    j = hld.down[i]
    seg1.set(j, ab)
    seg2.set(j, ab)
seg1.build()
seg2.build()
for _ in range(Q):
    cmd = rd()
    if cmd:
        u, v, x = rd(), rd(), rd()
        ans = x
        def func(l: int, r: int) -> None:
            global ans
            if l <= r: ab = seg1.prod(l, r)
            else: ab = seg2.prod(r, l)
            ans = ((ab >> 30) * ans + (ab & 0x3fffffff)) % mod
        hld.path_noncommutative_query(u, v, 1, func)
        wtn(ans)
    else:
        p, c, d = rd(), rd(), rd()
        i = hld.down[p]
        seg1.update(i, c << 30 | d)
        seg2.update(i, c << 30 | d)