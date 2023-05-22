# https://judge.yosupo.jp/problem/range_affine_range_sum
# my module
from misc.fastio import *
from segment_tree.lazy_segment_tree import *
# my module
mod = 998244353
mask = (1 << 30) - 1
def op(x: int, y: int) -> int:
    return x + y - mod if x + y >= mod else x + y
def mapping(x: int, length: int, F: int) -> int:
    a, b = F >> 30, F & mask
    return (a * x + b * length) % mod
def composition(F: int, G: int) -> int:
    a, b = F >> 30, F & mask
    c, d = G >> 30, G & mask
    e, f = a * c % mod, (a * d + b) % mod
    return e << 30 | f
N, Q = rd(), rd()
A = rdl(N)
seg = LazySegmentTree(N, 0, 1 << 30, op, mapping, composition, A)
for _ in range(Q):
    cmd = rd()
    if cmd:
        l, r = rd(), rd()
        wtn(seg.prod(l, r))
    else:
        l, r, b, c = rd(), rd(), rd(), rd()
        seg.range_apply(l, r, b << 30 | c)