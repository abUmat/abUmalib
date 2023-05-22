# https://judge.yosupo.jp/problem/point_set_range_composite
# my module
from misc.fastio import *
from segment_tree.segment_tree import *
# my module
mod = 998244353
mask = (1 << 30) - 1
def op(x: int, y: int) -> int:
    a, b = x >> 30, x & mask
    c, d = y >> 30, y & mask
    e, f = a * c % mod, (c * b + d) % mod
    return e << 30 | f
N, Q = rd(), rd()
A = [rd() << 30 | rd() for _ in range(N)]
seg = SegmentTree(N, 1 << 30, op, A)
for _ in range(Q):
    cmd = rd()
    if cmd:
        l, r, x = rd(), rd(), rd()
        ab = seg.prod(l, r)
        a, b = ab >> 30, ab & mask
        wtn((a * x + b) % mod)
    else:
        p, c, d = rd(), rd(), rd()
        seg.update(p, c << 30 | d)