from bisect import bisect_left as lower_bound
# my module
from segment_tree.segment_tree import *
# my module
class RangeTree:
    """
    e: identity element of op
    op: operator merge
    """
    def __init__(self, e: int, op):
        self.e = e
        self.op = op
        self.ps = []

    def add_point(self, x: int, y: int) -> None:
        'add point (x, y) for initialize'
        self.ps.append(x << 30 | y)
        # self.ps.append((x, y))

    def build(self) -> None:
        'initialize'
        mask = (1 << 30) -1; e = self.e; op = self.op
        self.ps = ps = sorted(set(self.ps))
        self.xs = [p >> 30 for p in ps]
        self.N = N = len(ps)
        self.ys = ys = [0] * (N << 1)
        self.seg = seg = [0] * (N << 1)
        ys[N:] = [[p & mask] for p in ps]
        for i in range(1, N)[::-1]: ys[i] = sorted(set(ys[i << 1] + ys[i << 1 | 1]))
        seg[1:N] = [SegmentTree(len(y), e, op) for y in ys[1:N]]
        seg[N:] = [SegmentTree(1, e, op) for _ in range(N)]

    def add(self, x: int, y: int, a: int) -> None:
        seg = self.seg; ys = self.ys
        i = lower_bound(self.ps, x << 30 | y)
        i += self.N
        while i:
            seg[i].add(lower_bound(ys[i], y), a)
            i >>= 1

    def sum(self, xl: int, yl: int, xr: int, yr: int) -> int:
        L = R = self.e; op = self.op; seg = self.seg; ys = self.ys
        a = lower_bound(self.xs, xl); b = lower_bound(self.xs, xr)
        a += self.N; b += self.N
        while a < b:
            if a & 1:
                L = op(L, seg[a].prod(lower_bound(ys[a], yl), lower_bound(ys[a], yr)))
                a += 1
            if b & 1:
                b ^= 1
                R = op(seg[b].prod(lower_bound(ys[b], yl), lower_bound(ys[b], yr)), R)
            a >>= 1; b >>= 1
        return op(L, R)
